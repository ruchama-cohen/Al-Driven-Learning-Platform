from fastapi import APIRouter, HTTPException
from config import db
from schemas import SubCategory
from bson import ObjectId

router = APIRouter()
sub_categories_collection = db["sub_categories"]

@router.post("/sub-categories")
def create_sub_category(sub_category: SubCategory):
    """Create new sub-category"""
    try:
        print(f"Creating sub-category: {sub_category.name} for category: {sub_category.category_id}")
        
        result = sub_categories_collection.insert_one({
            "name": sub_category.name,
            "category_id": sub_category.category_id
        })
        
        print(f"Sub-category created successfully with ID: {result.inserted_id}")
        
        return {
            "success": True,
            "id": str(result.inserted_id),
            "name": sub_category.name,
            "category_id": sub_category.category_id,
            "message": "Sub-category created successfully"
        }
        
    except Exception as e:
        print(f"Error creating sub-category: {e}")
        raise HTTPException(status_code=500, detail=f"Error creating sub-category: {str(e)}")

@router.get("/sub-categories")
def list_sub_categories():
    """Get list of all sub-categories"""
    try:
        sub_categories = list(sub_categories_collection.find({}))
        
        for sub_category in sub_categories:
            sub_category["id"] = str(sub_category["_id"])
            del sub_category["_id"]
            
        print(f"Retrieved {len(sub_categories)} sub-categories")
        return sub_categories
        
    except Exception as e:
        print(f"Error fetching sub-categories: {e}")
        raise HTTPException(status_code=500, detail="Error fetching sub-categories")

@router.get("/categories/{category_id}/sub-categories")
def get_sub_categories_by_category(category_id: str):
    """Get sub-categories for a specific category"""
    try:
        sub_categories = list(sub_categories_collection.find({"category_id": category_id}))
        
        for sub_category in sub_categories:
            sub_category["id"] = str(sub_category["_id"])
            del sub_category["_id"]
            
        print(f"Retrieved {len(sub_categories)} sub-categories for category {category_id}")
        return sub_categories
        
    except Exception as e:
        print(f"Error fetching sub-categories for category {category_id}: {e}")
        raise HTTPException(status_code=500, detail="Error fetching sub-categories")

@router.get("/sub-categories/{sub_category_id}")
def get_sub_category(sub_category_id: str):
    """Get single sub-category details"""
    try:
        sub_category = sub_categories_collection.find_one({"_id": ObjectId(sub_category_id)})
        
        if not sub_category:
            raise HTTPException(status_code=404, detail="Sub-category not found")
            
        sub_category["id"] = str(sub_category["_id"])
        del sub_category["_id"]
        
        return sub_category
        
    except ObjectId.InvalidId:
        raise HTTPException(status_code=400, detail="Invalid sub-category ID format")
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error fetching sub-category {sub_category_id}: {e}")
        raise HTTPException(status_code=500, detail="Error fetching sub-category")

@router.delete("/sub-categories/{sub_category_id}")
def delete_sub_category(sub_category_id: str):
    """Delete sub-category"""
    try:
        result = sub_categories_collection.delete_one({"_id": ObjectId(sub_category_id)})
        
        if result.deleted_count == 0:
            raise HTTPException(status_code=404, detail="Sub-category not found")
            
        print(f"Sub-category {sub_category_id} deleted successfully")
        
        return {
            "success": True,
            "message": "Sub-category deleted successfully"
        }
        
    except ObjectId.InvalidId:
        raise HTTPException(status_code=400, detail="Invalid sub-category ID format")
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error deleting sub-category {sub_category_id}: {e}")
        raise HTTPException(status_code=500, detail="Error deleting sub-category")