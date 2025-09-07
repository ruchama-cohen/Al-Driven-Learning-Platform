import os
from pymongo import MongoClient
from dotenv import load_dotenv
from pathlib import Path

# טוען את .env מהתיקייה החיצונית (אחת מעל app/)
env_path = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(dotenv_path=env_path)

print("DEBUG MONGO_URI =", os.getenv("MONGO_URI"))

client = MongoClient(os.getenv("MONGO_URI"))
db = client[os.getenv("MONGO_DB")]
