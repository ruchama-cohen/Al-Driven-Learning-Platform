from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from config import db
import uuid

router = APIRouter()
categories_collection = db["categories"]
subcategories_collection = db["sub_categories"]

class Category(BaseModel):
    name: str

class SubCategory(BaseModel):
    name: str
    category_id: str

@router.post("/categories")
def create_category(category: Category):
    category_dict = category.dict()
    category_dict["id"] = str(uuid.uuid4())
    categories_collection.insert_one(category_dict)
    return {"id": category_dict["id"], "message": "Category created"}

@router.get("/categories")
def list_categories():
    return list(categories_collection.find({}, {"_id": 0}))

@router.post("/subcategories")
def create_subcategory(subcategory: SubCategory):
    if not categories_collection.find_one({"id": subcategory.category_id}):
        raise HTTPException(status_code=404, detail="Category not found")

    subcategory_dict = subcategory.dict()
    subcategory_dict["id"] = str(uuid.uuid4())
    subcategories_collection.insert_one(subcategory_dict)
    return {"id": subcategory_dict["id"], "message": "Subcategory created"}

@router.get("/subcategories")
def list_subcategories():
    return list(subcategories_collection.find({}, {"_id": 0}))
