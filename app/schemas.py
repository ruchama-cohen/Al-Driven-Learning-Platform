from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class User(BaseModel):
    name: str
    phone: str
    id_number: str

class Token(BaseModel):
    access_token: str
    token_type: str
    user_id: str
    name: str
    id_number: Optional[str] 

class Category(BaseModel):
    name: str

class SubCategory(BaseModel):
    name: str
    category_id: str

class PromptRequest(BaseModel):
    user_id: str
    category_id: str
    sub_category_id: str
    prompt: str

class PromptResponse(BaseModel):
    id: str
    user_id: str
    category_id: str
    sub_category_id: str
    prompt: str
    response: str
    created_at: datetime
    password: str

class UserLogin(BaseModel):
    id: str
    password: str