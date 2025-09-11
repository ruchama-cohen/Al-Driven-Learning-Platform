from pydantic import BaseModel, Field, validator
from typing import Optional, List
from datetime import datetime

class User(BaseModel):
    name: str = Field(..., min_length=2, max_length=50)
    phone: str = Field(..., min_length=9, max_length=15)
    id_number: str = Field(..., min_length=5, max_length=12)
    
    @validator('phone')
    def validate_phone(cls, v):
        v = v.replace('-', '').replace(' ', '')
        if not v.isdigit():
            raise ValueError('Phone must contain only digits')
        return v

class UserResponse(BaseModel):
    id: str
    name: str
    phone: str
    id_number: str
    created_at: datetime

class Token(BaseModel):
    access_token: str
    token_type: str
    user_id: str
    name: str
    id_number: Optional[str] = None

class TokenData(BaseModel):
    user_id: Optional[str] = None

class UserLogin(BaseModel):
    name: str
    phone: str
    id_number: str

class Category(BaseModel):
    name: str = Field(..., min_length=2, max_length=50)

class CategoryResponse(BaseModel):
    id: str
    name: str

class SubCategory(BaseModel):
    name: str = Field(..., min_length=2, max_length=50)
    category_id: str

class SubCategoryResponse(BaseModel):
    id: str
    name: str
    category_id: str

class PromptRequest(BaseModel):
    user_id: str
    category_id: Optional[str] = None
    sub_category_id: Optional[str] = None
    prompt: str = Field(..., min_length=5, max_length=1000)

class PromptResponse(BaseModel):
    id: str
    user_id: str
    category_id: Optional[str]
    sub_category_id: Optional[str]
    prompt: str
    response: str
    created_at: datetime

class PaginationParams(BaseModel):
    page: int = Field(1, ge=1)
    limit: int = Field(10, ge=1, le=100)
    search: Optional[str] = None
    sort_by: str = "created_at"
    sort_order: str = "desc"

class PaginatedResponse(BaseModel):
    items: List
    total: int
    page: int
    limit: int
    pages: int
    has_next: bool
    has_prev: bool

class UsersPaginatedResponse(PaginatedResponse):
    items: List[UserResponse] = Field(alias="users")

class ErrorResponse(BaseModel):
    success: bool = False
    error: str
    detail: Optional[str] = None

class SuccessResponse(BaseModel):
    success: bool = True
    message: str
    data: Optional[dict] = None