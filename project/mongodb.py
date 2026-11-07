from pymongo import MongoClient

MONGO_URI = "mongodb+srv://<db_username>:<db_password>@cluster0.cdukerv.mongodb.net/"
MONGO_DB_NAME = "website"

client = MongoClient(MONGO_URI)

db = client[MONGO_DB_NAME]

categories_collection = db["category"]
contact_collection = db["contact_collection"]