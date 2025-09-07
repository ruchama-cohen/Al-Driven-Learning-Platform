import certifi
import os
from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()

uri = os.getenv("MONGODB_URI")
client = MongoClient(uri, tls=True, tlsCAFile=certifi.where())
db = client["learning_platform"]

users = db["users"]

result = users.insert_one({
    "name": "Israel",
    "phone": "050-1234567"
})

print("Document inserted with ID:", result.inserted_id)


for u in users.find():
    print(u)
