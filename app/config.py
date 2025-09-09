import os
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")
MONGO_DB = os.getenv("MONGO_DB")

if not MONGO_URI:
    raise ValueError("MONGO_URI not found in .env file")
if not MONGO_DB:
    raise ValueError("MONGO_DB not found in .env file")

print(f"DEBUG MONGO_URI = {MONGO_URI}")
print(f"DEBUG MONGO_DB = {MONGO_DB}")

try:
    client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=10000)
    client.admin.command('ping')
    print("MongoDB Atlas connected successfully!")
    db = client[MONGO_DB]
except Exception as e:
    print(f"MongoDB connection failed: {e}")
    raise Exception(f"Cannot connect to MongoDB: {e}")