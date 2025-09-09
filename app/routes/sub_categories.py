from fastapi import APIRouter, HTTPException
from config import db
from schemas import SubCategory
from bson import ObjectId

router = APIRouter()
sub_categories_collection = db["sub_categories"]

@router.post("/sub-categories")
def create_sub_category(sub_category: SubCategory):
    result = sub_categories_collection.insert_one(sub_category.dict())
    return {"id": str(result.inserted_id), "message": "Sub-category created successfully"}

@router.get("/sub-categories")
def list_sub_categories():
    sub_categories = list(sub_categories_collection.find({}))
    for sub_category in sub_categories:
        sub_category["id"] = str(sub_category["_id"])
        del sub_category["_id"]
    return sub_categories

@router.get("/categories/{category_id}/sub-categories")
def get_sub_categories_by_category(category_id: str):
    sub_categories = list(sub_categories_collection.find({"category_id": category_id}))
    for sub_category in sub_categories:
        sub_category["id"] = str(sub_category["_id"])
        del sub_category["_id"]
    return sub_categories