from pymongo import MongoClient

MONGO_URI = "mongodb://localhost:27017/"
MONGO_DB_NAME = "website"

client = MongoClient(MONGO_URI)

db = client[MONGO_DB_NAME]

categories_collection = db["category"]
contact_collection = db["contact_collection"]