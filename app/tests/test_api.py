import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_health_endpoint():
    """Test that health endpoint works"""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"

def test_register_user():
    """Test user registration"""
    import random
    unique_id = str(random.randint(100000, 999999))
    user_data = {
        "name": f"Test User {unique_id}",
        "phone": f"123{unique_id}", 
        "id_number": f"999{unique_id}"
    }
    response = client.post("/api/users/register", json=user_data)
    assert response.status_code == 200
    data = response.json()
    assert data["success"] == True
    assert f"Test User {unique_id}" in data["name"]

def test_login_user():
    """Test user login"""
    import random
    unique_id = str(random.randint(100000, 999999))
    user_data = {
        "name": f"Login Test {unique_id}",
        "phone": f"987{unique_id}",
        "id_number": f"888{unique_id}"
    }
    # First register
    reg_response = client.post("/api/users/register", json=user_data)
    assert reg_response.status_code == 200
    
    # Then login
    response = client.post("/api/users/login", json=user_data)
    assert response.status_code == 200
    data = response.json()
    assert "id" in data
    assert data["message"] == "Login successful"

def test_get_categories():
    """Test getting categories"""
    response = client.get("/api/categories")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)

def test_create_category():
    """Test creating a category"""
    category_data = {"name": "Test Category"}
    response = client.post("/api/categories", json=category_data)
    assert response.status_code == 200

def test_create_lesson():
    """Test creating AI lesson"""
    # First create a user
    import random
    unique_id = str(random.randint(100000, 999999))
    user_data = {
        "name": f"Lesson User {unique_id}",
        "phone": f"555{unique_id}",
        "id_number": f"777{unique_id}"
    }
    user_response = client.post("/api/users/register", json=user_data)
    user_id = user_response.json()["id"]
    
    lesson_data = {
        "user_id": user_id,
        "prompt": "Test lesson about math"
    }
    response = client.post("/api/prompts", json=lesson_data)
    assert response.status_code == 200
    data = response.json()
    assert "response" in data
    assert "math" in data["response"]