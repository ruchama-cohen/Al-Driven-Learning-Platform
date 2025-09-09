from fastapi import APIRouter, HTTPException
from config import db
from schemas import PromptRequest
from services.ai_service import generate_lesson
from bson import ObjectId
from datetime import datetime

router = APIRouter()
prompts_collection = db["prompts"]
categories_collection = db["categories"]
sub_categories_collection = db["sub_categories"]

@router.post("/prompts")
async def create_prompt(prompt_request: PromptRequest):
    """Create new lesson"""
    try:
        print(f"Creating new lesson for user: {prompt_request.user_id}")
        print(f"Category: {prompt_request.category_id}, Sub-category: {prompt_request.sub_category_id}")
        print(f"Question: {prompt_request.prompt}")
        
        category_name = ""
        sub_category_name = ""
        
        try:
            if prompt_request.category_id:
                category = categories_collection.find_one({"_id": ObjectId(prompt_request.category_id)})
                category_name = category["name"] if category else ""
                
            if prompt_request.sub_category_id:
                sub_category = sub_categories_collection.find_one({"_id": ObjectId(prompt_request.sub_category_id)})
                sub_category_name = sub_category["name"] if sub_category else ""
        except:
            if prompt_request.category_id:
                category = categories_collection.find_one({"_id": prompt_request.category_id})
                category_name = category["name"] if category else ""
                
            if prompt_request.sub_category_id:
                sub_category = sub_categories_collection.find_one({"_id": prompt_request.sub_category_id})
                sub_category_name = sub_category["name"] if sub_category else ""
        
        ai_response = await generate_lesson(prompt_request.prompt)
        
        prompt_doc = {
            "user_id": prompt_request.user_id,
            "category_id": prompt_request.category_id,
            "sub_category_id": prompt_request.sub_category_id,
            "prompt": prompt_request.prompt,
            "response": ai_response,
            "created_at": datetime.utcnow()
        }
        
        result = prompts_collection.insert_one(prompt_doc)
        
        print("Lesson created successfully")
        
        return {
            "success": True,
            "id": str(result.inserted_id),
            "response": ai_response,
            "message": "Lesson generated successfully"
        }
        
    except Exception as e:
        print(f"Error creating lesson: {e}")
        raise HTTPException(status_code=500, detail=f"Error generating lesson: {str(e)}")

@router.get("/users/{user_id}/prompts")
def get_user_prompts(user_id: str):
    """Get all lessons for a user"""
    try:
        prompts = list(prompts_collection.find({"user_id": user_id}).sort("created_at", -1))
        
        for prompt in prompts:
            prompt["id"] = str(prompt["_id"])
            del prompt["_id"]
            
        return prompts
        
    except Exception as e:
        print(f"Error fetching user prompts: {e}")
        raise HTTPException(status_code=500, detail="Error fetching user learning history")

@router.get("/prompts")
def list_all_prompts():
    """Get all lessons (for admin dashboard)"""
    try:
        prompts = list(prompts_collection.find({}).sort("created_at", -1))
        
        for prompt in prompts:
            prompt["id"] = str(prompt["_id"])
            del prompt["_id"]
            
        return prompts
        
    except Exception as e:
        print(f"Error fetching all prompts: {e}")
        raise HTTPException(status_code=500, detail="Error fetching prompts")

@router.get("/prompts/{prompt_id}")
def get_prompt(prompt_id: str):
    """Get single lesson"""
    try:
        prompt = prompts_collection.find_one({"_id": ObjectId(prompt_id)})
        
        if not prompt:
            raise HTTPException(status_code=404, detail="Lesson not found")
            
        prompt["id"] = str(prompt["_id"])
        del prompt["_id"]
        
        return prompt
        
    except Exception as e:
        print(f"Error fetching prompt: {e}")
        raise HTTPException(status_code=500, detail="Error fetching lesson")