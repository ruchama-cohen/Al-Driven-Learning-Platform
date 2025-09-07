from fastapi import APIRouter
from pydantic import BaseModel
from config import db
import uuid, datetime

router = APIRouter()
prompts_collection = db["prompts"]

class PromptRequest(BaseModel):
    user_id: str
    category_id: str
    sub_category_id: str
    prompt: str

@router.post("/prompts")
def create_prompt(req: PromptRequest):
    response_text = f"📘 This is a mock lesson about: {req.prompt}"


    prompt_doc = {
        "id": str(uuid.uuid4()),
        "user_id": req.user_id,
        "category_id": req.category_id,
        "sub_category_id": req.sub_category_id,
        "prompt": req.prompt,
        "response": response_text,
        "created_at": datetime.datetime.utcnow()
    }
    prompts_collection.insert_one(prompt_doc)

    return {"id": prompt_doc["id"], "response": response_text}

@router.get("/users/{user_id}/prompts")
def get_user_prompts(user_id: str):
    history = list(prompts_collection.find({"user_id": user_id}, {"_id": 0}))
    return history
