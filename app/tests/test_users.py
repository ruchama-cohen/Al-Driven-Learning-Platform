import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_health_check():
    """Test health endpoint"""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"

def test_register_user():
    """Test user registration"""
    user_data = {
        "name": "Test User",
        "phone": "1234567890",
        "id_number": "123456789"
    }
    response = client.post("/api/users/register", json=user_data)
    assert response.status_code == 200
    data = response.json()
    assert data["success"] == True
    assert data["name"] == "Test User"

def test_login_user():
    """Test user login with JWT"""
    # First register a user
    user_data = {
        "name": "Login Test User",
        "phone": "9876543210",
        "id_number": "987654321"
    }
    client.post("/api/users/register", json=user_data)
    
    # Then login
    response = client.post("/api/users/login", json=user_data)
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"

def test_get_users_pagination():
    """Test users pagination"""
    response = client.get("/api/users?page=1&limit=5")
    assert response.status_code == 200
    data = response.json()
    assert "users" in data
    assert "total" in data
    assert "page" in data
    assert "limit" in data

def test_create_category():
    """Test category creation"""
    category_data = {"name": "Test Category"}
    response = client.post("/api/categories", json=category_data)
    assert response.status_code == 200

def test_get_categories():
    """Test get categories"""
    response = client.get("/api/categories")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)