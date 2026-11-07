from pymongo import MongoClient

MONGO_URI = "mongodb+srv://aiswaryabalu88_db_user:mu7L0fdRWYcvyMbU@cluster0.cdukerv.mongodb.net/"
MONGO_DB_NAME = "website"

client = MongoClient(MONGO_URI)

db = client[MONGO_DB_NAME]

categories_collection = db["category"]
contact_collection = db["contact_collection"]