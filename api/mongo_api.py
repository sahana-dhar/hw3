"""
mongo_api.py
California Infectious Disease Surveillance API
Provides 3-4 parameterized query functions over the epidemiology MongoDB database.
A data scientist can use these functions without knowing MongoDB or MQL.

Contributions: Anya Wild
"""
from pymongo import MongoClient

# Connection setup
client = MongoClient("mongodb://localhost:27017")
db = client["epidemiology"]
collection = db["infectious_diseases"]

'''
returns: true if disease exists
'''
def disease_exists(disease):
    # check disease has records
    most_recent = collection.find_one(
        {"disease": disease}
    )
    if not most_recent:
        print("Disease not found!")
        return False
    else:
        return True


'''
returns: top counties (10 default) affected by given disease, according to total num cases
'''
def get_affected_counties(disease, num=10):
    if not disease_exists(disease):
        return ""
    
    # set up pipeline
    pipeline = [
        {"$match": {"disease": disease,
            "demographics.sex": "Total",
            "location.county": {"$ne": "California"} # "California" is placeholder county
        }},
        {"$group":{
            "_id": "$location.county",
            "total_cases": {"$sum": "$stats.cases"}
        }},
        {"$sort": {"total_cases": -1}},
        {"$limit": num} # limit by given number
    ]

    return list(collection.aggregate(pipeline))


'''
returns: yearly statewide counts of a given disease (5 years default) 
'''
def get_disease_trend(disease, years=5):
    if not disease_exists(disease):
        return ""
    
    # find most recent entry and calculate the minimum year from that entry
    most_recent = collection.find_one(
        {"disease": disease},
        sort=[("demographics.year", -1)]
    )
    min_year = most_recent["demographics"]["year"] - years

    # set up pipeline
    pipeline = [
        {"$match": {"disease": disease,
            "demographics.sex": "Total",
            "location.county": "California", # statewide total has county value "California"
            "demographics.year": 
                {"$gte": min_year} # only records >= given # of years
            }},
        {"$group": {
            "_id": "$demographics.year", 
            "total_cases": {"$sum": "$stats.cases"} # group by year and sum total # cases each year
        }},
        {"$sort": {"_id": -1}} # orders by year
    ]

    return list(collection.aggregate(pipeline))


'''
returns: given county's most prevelant diseases (3 default)
'''
def get_county_disease(county, num=3):
    # check for county
    county_exists = collection.find_one(
        {"location.county": county}
    )
    if not county_exists:
        print("County not found!")
        return list()
    
    # set up pipeline
    pipeline = [
        {"$match": {
            "location.county": county,
            "demographics.sex": "Total"
        }},
        {"$group": {
            "_id": "$disease",
            "total_cases": {"$sum": "$stats.cases"}
        }},
        {"$sort": {"total_cases": -1}},
        {"$limit": num} # limit by given number
    ]

    return list(collection.aggregate(pipeline))


if __name__ == "__main__":

    print("Top 5 Counties Affected by Amebiasis Disease")
    for r in get_affected_counties("Amebiasis", 5):
        print(f"  {r['_id']}: {r['total_cases']} cases")

    print("Salmonellosis Trends over 5 years")
    for r in get_disease_trend("Salmonellosis", 5):
        print(f"  {r['_id']}: {r['total_cases']} cases")

    print("Top 5 Dieases in Sacramento")
    for r in get_county_disease("Sacramento", 5):
        print(f"  {r['_id']}: {r['total_cases']} cases")