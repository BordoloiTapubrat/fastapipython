from pymongo import MongoClient

MONGO_URI: str="mongodb://localhost:27017/getnotes"

conn = MongoClient(MONGO_URI)