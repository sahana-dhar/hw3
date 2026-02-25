"""
visualize.py
California Infectious Disease Surveillance API
Visualizes output of the get_disease_trend function from our API

Contributions: Anya Wild
"""

import matplotlib.pyplot as plt
from mongo_api import get_disease_trend

def plot_disease_trend(disease, years=5):
    
    # call get_disease_trend from API
    data = get_disease_trend(disease, years)

    # get years and case totals for x and y
    x_years = [r["_id"] for r in data]
    y_cases = [r["total_cases"] for r in data]

    # plot on graph
    plt.figure(figsize=(10, 5))
    plt.plot(x_years, y_cases, marker="o", linewidth=2)
    plt.title(f"{disease} Cases in California Over {years} Years")
    plt.xlabel("Year")
    plt.ylabel("Total Cases")
    plt.show()

if __name__ == "__main__":
    plot_disease_trend("Salmonellosis", 10)