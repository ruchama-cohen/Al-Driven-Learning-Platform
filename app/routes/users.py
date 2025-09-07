from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from config import db

router = APIRouter()
users_collection = db["users"]

class User(BaseModel):
    id: str     
    name: str
    phone: str

@router.post("/users")
def create_user(user: User):
    if users_collection.find_one({"id": user.id}):
        raise HTTPException(status_code=400, detail="User with this ID already exists")

    result = users_collection.insert_one(user.dict())
    return {"id": user.id, "message": "User created successfully"}

@router.get("/users")
def list_users():
    users = list(users_collection.find({}, {"_id": 0}))
    return users

@router.get("/users/{id}")
def get_user(id: str):
    user = users_collection.find_one({"id": id}, {"_id": 0})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user
