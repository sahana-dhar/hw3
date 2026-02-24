"""
mongo_api.py
California Infectious Disease Surveillance API
Provides 3-4 parameterized query functions over the epidemiology MongoDB database.
A data scientist can use these functions without knowing MongoDB or MQL.
"""
from pymongo import MongoClient
