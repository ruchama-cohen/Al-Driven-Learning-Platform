from fastapi import APIRouter, HTTPException
from config import db
from schemas import User, UserLogin
from bson import ObjectId

router = APIRouter()
users_collection = db["users"]

@router.post("/users/register")
def register_user(user: User):
    existing_user = users_collection.find_one({"phone": user.phone})
    if existing_user:
        raise HTTPException(status_code=400, detail="User with this phone already exists")
    result = users_collection.insert_one(user.dict())
    return {
        "id": str(result.inserted_id),
        "name": user.name,
        "phone": user.phone,
        "message": "User registered successfully"
    }

@router.post("/users/login")
def login_user(login_data: UserLogin):
    user = users_collection.find_one({
        "name": login_data.name,
        "phone": login_data.phone
    })
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found. Please register first.")
    
    return {
        "id": str(user["_id"]),
        "name": user["name"],
        "phone": user["phone"],
        "message": "Login successful"
    }

@router.get("/users")
def list_users():
    users = list(users_collection.find({}))
    for user in users:
        user["id"] = str(user["_id"])
        del user["_id"]
    return users

@router.get("/users/{user_id}")
def get_user(user_id: str):
    user = users_collection.find_one({"_id": ObjectId(user_id)})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    user["id"] = str(user["_id"])
    del user["_id"]
    return user
