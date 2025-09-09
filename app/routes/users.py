from fastapi import APIRouter, HTTPException, Request
from config import db
from schemas import User
from bson import ObjectId
from datetime import datetime

router = APIRouter()
users_collection = db["users"]

@router.post("/users")
def create_user(user: User):
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
    
    result = users_collection.insert_one(user.dict())
    return {
        "id": str(result.inserted_id),
        "name": user.name,
        "phone": user.phone,
        "id_number": user.id_number,
        "message": "User registered successfully"
    }

@router.post("/users/register-only")
def register_only(user: User):
    existing_user = users_collection.find_one({"phone": user.phone})
    if existing_user:
        raise HTTPException(status_code=400, detail="User already exists. Please use login.")
    
    result = users_collection.insert_one(user.dict())
    return {
        "id": str(result.inserted_id),
        "name": user.name,
        "phone": user.phone,
        "message": "User registered successfully"
    }

@router.post("/users/login-only")
def login_only(user: User):
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
        raise HTTPException(status_code=404, detail="User not found. Please check your details or register first.")
    
    return {
        "id": str(existing_user["_id"]),
        "name": existing_user["name"],
        "phone": existing_user["phone"],
        "id_number": existing_user.get("id_number", ""),
        "message": "Login successful"
    }

@router.get("/users")
def list_users():
    """Get list of all users (for admin)"""
    try:
        print("=== LIST USERS REQUEST ===")
        users = list(users_collection.find({}).sort("created_at", -1))
        
        for user in users:
            user["id"] = str(user["_id"])
            del user["_id"]
            
        print(f"Retrieved {len(users)} users")
        return users
        
    except Exception as e:
        print(f"Error fetching users: {e}")
        raise HTTPException(status_code=500, detail="Error fetching users list")

@router.get("/users/{user_id}")
def get_user(user_id: str):
    """Get single user details"""
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

@router.post("/users/login")
async def login_user(user: User, request: Request):
    """Login existing user"""
    try:
        print(f"=== LOGIN USER REQUEST ===")
        print(f"Method: {request.method}")
        print(f"URL: {request.url}")
        print(f"Headers: {dict(request.headers)}")
        print(f"User data: {user}")
        print(f"Logging in user: {user.name} ({user.phone})")
        
        existing_user = users_collection.find_one({
            "name": user.name,
            "phone": user.phone,
            "id_number": user.id_number
        })
        
        if not existing_user:
            print(f"User not found: {user.name} ({user.phone})")
            raise HTTPException(
                status_code=404, 
                detail="User not found. Please check your details or register first."
            )
        
        print(f"User logged in successfully: {existing_user['_id']}")
        
        response_data = {
            "success": True,
            "id": str(existing_user["_id"]),
            "name": existing_user["name"],
            "phone": existing_user["phone"],
            "id_number": existing_user["id_number"],
            "message": "Login successful"
        }
        
        print(f"Returning response: {response_data}")
        return response_data
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error logging in user: {e}")
        raise HTTPException(status_code=500, detail="Error logging in user")

@router.post("/users/register")
async def register_user(user: User, request: Request):
    """Register new user"""
    try:
        print(f"=== REGISTER USER REQUEST ===")
        print(f"Method: {request.method}")
        print(f"URL: {request.url}")
        print(f"Headers: {dict(request.headers)}")
        print(f"User data: {user}")
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
        
        print(f"User registered successfully with ID: {result.inserted_id}")
        
        response_data = {
            "success": True,
            "id": str(result.inserted_id),
            "name": user.name,
            "phone": user.phone,
            "id_number": user.id_number,
            "message": "User registered successfully"
        }
        
        print(f"Returning response: {response_data}")
        return response_data
        
    except Exception as e:
        print(f"Error registering user: {e}")
        raise HTTPException(status_code=500, detail="Error registering user")

@router.get("/users/debug/test")
def test_users_endpoint():
    """Test endpoint to verify users router is working"""
    return {
        "message": "Users router is working",
        "router": "users",
        "available_endpoints": [
            "POST /api/users/register",
            "POST /api/users/login", 
            "GET /api/users",
            "GET /api/users/{user_id}"
        ]
    }