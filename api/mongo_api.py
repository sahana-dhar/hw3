"""
mongo_api.py
California Infectious Disease Surveillance API
Provides 3-4 parameterized query functions over the epidemiology MongoDB database.
A data scientist can use these functions without knowing MongoDB or MQL.
"""
from pymongo import MongoClient

# Connection setup
client = MongoClient("mongodb://localhost:27017")
db = client["epidemiology"]
collection = db["infectious_diseases"]

def test_connection():
    count = collection.count_documents({})
    print(f"Found {count} records in infectious_diseases collection.")

if __name__ == "__main__":
    test_connection()