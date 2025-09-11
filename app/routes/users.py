from fastapi import APIRouter, HTTPException, Depends, Query
from config import db
from schemas import User, Token, UserLogin
from auth import create_access_token, verify_token
from bson import ObjectId
from datetime import datetime, timedelta

router = APIRouter()
users_collection = db["users"]

@router.post("/users/register", response_model=Token)
def register_user(user: User):
    try:
        print(f"=== REGISTER USER REQUEST ===")
        print(f"Registering new user: {user.name} ({user.phone})")

        existing_user = users_collection.find_one({"phone": user.phone})
        if existing_user:
            print(f"User already exists with phone: {user.phone}")
            raise HTTPException(
                status_code=400, 
                detail="User with this phone number already exists"
            )
 
        existing_user_by_id = users_collection.find_one({"id_number": user.id_number})
        if existing_user_by_id:
            print(f"User already exists with ID number: {user.id_number}")
            raise HTTPException(
                status_code=400, 
                detail="User with this ID number already exists"
            )

        user_doc = {
            "name": user.name,
            "phone": user.phone,
            "id_number": user.id_number,
            "created_at": datetime.utcnow()
        }
        
        print(f"Inserting user document: {user_doc}")
        result = users_collection.insert_one(user_doc)
        
        access_token_expires = timedelta(minutes=30)
        access_token = create_access_token(
            data={"sub": str(result.inserted_id)}, 
            expires_delta=access_token_expires
        )
        
        print(f"User registered successfully with ID: {result.inserted_id}")
        
        return Token(
            access_token=access_token,
            token_type="bearer",
            user_id=str(result.inserted_id),
            name=user.name,
            id_number=user.id_number
        )
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error registering user: {e}")
        raise HTTPException(status_code=500, detail="Error registering user")

@router.post("/users/login", response_model=Token)
def login_user(user: User):
    try:
        print(f"=== LOGIN USER REQUEST ===")
        print(f"Login attempt for: {user.name} ({user.phone})")
        
        existing_user = users_collection.find_one({
            "name": user.name,
            "phone": user.phone,
            "id_number": user.id_number
        })

        if not existing_user:
            old_user = users_collection.find_one({
                "name": user.name,
                "phone": user.phone
            })
            
            if old_user and "id_number" not in old_user:
                users_collection.update_one(
                    {"_id": old_user["_id"]},
                    {"$set": {"id_number": user.id_number}}
                )
                existing_user = users_collection.find_one({"_id": old_user["_id"]})

        if not existing_user:
            print(f"User not found: {user.name} ({user.phone})")
            raise HTTPException(
                status_code=404,
                detail="User not found. Please check your details or register first."
            )

        access_token_expires = timedelta(minutes=30)
        access_token = create_access_token(
            data={"sub": str(existing_user["_id"])}, 
            expires_delta=access_token_expires
        )
        
        print(f"Login successful for user ID: {existing_user['_id']}")

        return Token(
            access_token=access_token,
            token_type="bearer",
            user_id=str(existing_user["_id"]),
            name=existing_user["name"],
            id_number=existing_user.get("id_number", "")
        )
            
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error logging in user: {e}")
        raise HTTPException(status_code=500, detail="Error logging in user")

@router.get("/users")
def list_users(
    page: int = Query(1, ge=1), 
    limit: int = Query(10, ge=1, le=100),
    search: str = Query(None),
    sort_by: str = Query("created_at", regex="^(name|phone|created_at)$"),
    sort_order: str = Query("desc", regex="^(asc|desc)$")
):
    try:
        skip = (page - 1) * limit

        query = {}
        if search:
            query = {
                "$or": [
                    {"name": {"$regex": search, "$options": "i"}},
                    {"phone": {"$regex": search, "$options": "i"}},
                    {"id_number": {"$regex": search, "$options": "i"}}
                ]
            }

        total = users_collection.count_documents(query)

        sort_direction = -1 if sort_order == "desc" else 1
        users = list(users_collection.find(query)
                    .sort(sort_by, sort_direction)
                    .skip(skip)
                    .limit(limit))
        
        for user in users:
            user["id"] = str(user["_id"])
            del user["_id"]
            
        return {
            "users": users,
            "total": total,
            "page": page,
            "limit": limit,
            "pages": (total + limit - 1) // limit,
            "has_next": page * limit < total,
            "has_prev": page > 1,
            "search": search,
            "sort_by": sort_by,
            "sort_order": sort_order
        }
        
    except Exception as e:
        print(f"Error fetching users: {e}")
        raise HTTPException(status_code=500, detail="Error fetching users list")

@router.get("/users/{user_id}")
def get_user(user_id: str):
    """קבלת פרטי משתמש בודד"""
    try:
        print(f"=== GET USER REQUEST === ID: {user_id}")
        user = users_collection.find_one({"_id": ObjectId(user_id)})
        
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
            
        user["id"] = str(user["_id"])
        del user["_id"]
        
        return user
        
    except ObjectId.InvalidId:
        raise HTTPException(status_code=400, detail="Invalid user ID format")
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error fetching user {user_id}: {e}")
        raise HTTPException(status_code=500, detail="Error fetching user details")

@router.get("/users/me/profile")
def get_current_user_profile(current_user_id: str = Depends(verify_token)):
    """קבלת פרופיל המשתמש המחובר"""
    try:
        user = users_collection.find_one({"_id": ObjectId(current_user_id)})
        
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
            
        user["id"] = str(user["_id"])
        del user["_id"]
        
        return user
        
    except Exception as e:
        print(f"Error fetching current user profile: {e}")
        raise HTTPException(status_code=500, detail="Error fetching user profile")

@router.delete("/users/{user_id}")
def delete_user(user_id: str):
    """מחיקת משתמש (למנהל)"""
    try:
        result = users_collection.delete_one({"_id": ObjectId(user_id)})
        
        if result.deleted_count == 0:
            raise HTTPException(status_code=404, detail="User not found")
        
        return {"message": "User deleted successfully"}
        
    except ObjectId.InvalidId:
        raise HTTPException(status_code=400, detail="Invalid user ID format")
    except Exception as e:
        print(f"Error deleting user: {e}")
        raise HTTPException(status_code=500, detail="Error deleting user")

@router.post("/users")
def legacy_create_user(user: User):
    """Legacy endpoint - מחזיר רק פרטי משתמש ללא JWT"""
    existing_user = users_collection.find_one({
        "name": user.name,
        "phone": user.phone,
        "id_number": user.id_number
    })
    
    if existing_user:
        return {
            "id": str(existing_user["_id"]),
            "name": existing_user["name"],
            "phone": existing_user["phone"],
            "id_number": existing_user["id_number"],
            "message": "User logged in successfully"
        }
    
    phone_exists = users_collection.find_one({"phone": user.phone})
    id_exists = users_collection.find_one({"id_number": user.id_number})
    
    if phone_exists:
        raise HTTPException(status_code=400, detail="Phone number already registered with different details")
    if id_exists:
        raise HTTPException(status_code=400, detail="ID number already registered with different details")
    
    result = users_collection.insert_one({
        "name": user.name,
        "phone": user.phone,
        "id_number": user.id_number,
        "created_at": datetime.utcnow()
    })
    return {
        "id": str(result.inserted_id),
        "name": user.name,
        "phone": user.phone,
        "id_number": user.id_number,
        "message": "User registered successfully"
    }

@router.get("/users/debug/test")
def test_users_endpoint():
    """טסט endpoint לוודא שהRouter עובד"""
    return {
        "message": "Users router is working",
        "router": "users",
        "available_endpoints": [
            "POST /api/users/register (returns JWT)",
            "POST /api/users/login (returns JWT)", 
            "GET /api/users (with pagination & filtering)",
            "GET /api/users/{user_id}",
            "GET /api/users/me/profile (JWT required)",
            "DELETE /api/users/{user_id}"
        ]
    }