import certifi
from pymongo import MongoClient

uri = "mongodb+srv://r0534104273_db_user:shIVVRY6D7X1Kibn@al-driven.em4ciff.mongodb.net/learning_platform?retryWrites=true&w=majority"
client = MongoClient(uri, tls=True, tlsCAFile=certifi.where())
db = client["learning_platform"]

# בחירת הקולקשן (אם לא קיים, הוא ייווצר אוטומטית)
users = db["users"]

# הכנסת מסמך חדש
result = users.insert_one({
    "name": "Israel",
    "phone": "050-1234567"
})

print("✅ Document inserted with ID:", result.inserted_id)

# קריאה של כל המשתמשים שהכנסנו
for u in users.find():
    print(u)
