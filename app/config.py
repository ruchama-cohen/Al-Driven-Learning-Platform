import os
from pymongo import MongoClient
from dotenv import load_dotenv
from pathlib import Path

env_path = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(dotenv_path=env_path)

print("DEBUG MONGO_URI =", os.getenv("MONGO_URI"))

import certifi

client = MongoClient(os.getenv("MONGO_URI"), tls=True, tlsCAFile=certifi.where())
db = client[os.getenv("MONGO_DB")]
