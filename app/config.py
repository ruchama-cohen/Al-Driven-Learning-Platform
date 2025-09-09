import os
from pymongo import MongoClient
from dotenv import load_dotenv
from pathlib import Path

env_path = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(dotenv_path=env_path)

print("DEBUG MONGO_URI =", os.getenv("MONGO_URI"))
print("DEBUG MONGO_DB =", os.getenv("MONGO_DB"))

import certifi

try:
    client = MongoClient(os.getenv("MONGO_URI"), tls=True, tlsCAFile=certifi.where())
    client.admin.command('ping')
    db = client[os.getenv("MONGO_DB")]
    print("MongoDB connected successfully!")
except Exception as e:
    print(f"MongoDB connection failed: {e}")
    client = MongoClient("mongodb://localhost:27017/")
    db = client["learning_platform_local"]
    print("Using local MongoDB fallback")