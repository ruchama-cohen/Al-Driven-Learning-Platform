from fastapi import APIRouter, HTTPException
from config import db
from schemas import PromptRequest, PromptResponse
from services.ai_service import generate_lesson, generate_mock_lesson
from bson import ObjectId
from datetime import datetime

router = APIRouter()
prompts_collection = db["prompts"]

@router.post("/prompts")
async def create_prompt(prompt_request: PromptRequest):
    ai_response = generate_mock_lesson(prompt_request.prompt)
    
    prompt_doc = {
        "user_id": prompt_request.user_id,
        "category_id": prompt_request.category_id,
        "sub_category_id": prompt_request.sub_category_id,
        "prompt": prompt_request.prompt,
        "response": ai_response,
        "created_at": datetime.utcnow()
    }
    
    result = prompts_collection.insert_one(prompt_doc)
    
    return {
        "id": str(result.inserted_id),
        "response": ai_response,
        "message": "Lesson generated successfully"
    }

@router.get("/users/{user_id}/prompts")
def get_user_prompts(user_id: str):
    prompts = list(prompts_collection.find({"user_id": user_id}))
    for prompt in prompts:
        prompt["id"] = str(prompt["_id"])
        del prompt["_id"]
    return prompts

@router.get("/prompts")
def list_all_prompts():
    prompts = list(prompts_collection.find({}))
    for prompt in prompts:
        prompt["id"] = str(prompt["_id"])
        del prompt["_id"]
    return prompts