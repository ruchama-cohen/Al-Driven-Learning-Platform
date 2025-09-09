from fastapi import APIRouter, HTTPException
from config import db
from schemas import Category
from bson import ObjectId

router = APIRouter()
categories_collection = db["categories"]

@router.post("/categories")
def create_category(category: Category):
    result = categories_collection.insert_one(category.dict())
    return {"id": str(result.inserted_id), "message": "Category created successfully"}

@router.get("/categories")
def list_categories():
    categories = list(categories_collection.find({}))
    for category in categories:
        category["id"] = str(category["_id"])
        del category["_id"]
    return categories

@router.get("/categories/{category_id}")
def get_category(category_id: str):
    category = categories_collection.find_one({"_id": ObjectId(category_id)})
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    category["id"] = str(category["_id"])
    del category["_id"]
    return category