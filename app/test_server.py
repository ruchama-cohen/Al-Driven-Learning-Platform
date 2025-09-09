from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Test server works!"}

@app.get("/api/test")
def test_endpoint():
    return {"status": "ok", "message": "API endpoint works"}

@app.post("/api/users")
def create_user(user: dict):
    return {"id": "test123", "message": "User created successfully"}

@app.get("/api/users")
def list_users():
    return [{"id": "test123", "name": "Test User", "phone": "123456789"}]

@app.get("/api/categories")
def list_categories():
    return [
        {"id": "cat1", "name": "Science"},
        {"id": "cat2", "name": "History"},
        {"id": "cat3", "name": "Technology"}
    ]

@app.post("/api/categories")
def create_category(category: dict):
    return {"id": "new_cat", "message": "Category created successfully"}

@app.get("/api/sub-categories")
def list_all_sub_categories():
    return [
        {"id": "sub1", "name": "Physics", "category_id": "cat1"},
        {"id": "sub2", "name": "Chemistry", "category_id": "cat1"},
        {"id": "sub3", "name": "Biology", "category_id": "cat1"},
        {"id": "sub4", "name": "Ancient History", "category_id": "cat2"},
        {"id": "sub5", "name": "Modern History", "category_id": "cat2"},
        {"id": "sub6", "name": "AI & Machine Learning", "category_id": "cat3"},
        {"id": "sub7", "name": "Web Development", "category_id": "cat3"}
    ]

@app.post("/api/sub-categories")
def create_sub_category(sub_category: dict):
    return {"id": "new_sub", "message": "Sub-category created successfully"}

@app.get("/api/categories/{category_id}/sub-categories")
def list_sub_categories(category_id: str):
    if category_id == "cat1":  
        return [
            {"id": "sub1", "name": "Physics", "category_id": "cat1"},
            {"id": "sub2", "name": "Chemistry", "category_id": "cat1"},
            {"id": "sub3", "name": "Biology", "category_id": "cat1"}
        ]
    elif category_id == "cat2":  
        return [
            {"id": "sub4", "name": "Ancient History", "category_id": "cat2"},
            {"id": "sub5", "name": "Modern History", "category_id": "cat2"}
        ]
    elif category_id == "cat3":  
        return [
            {"id": "sub6", "name": "AI & Machine Learning", "category_id": "cat3"},
            {"id": "sub7", "name": "Web Development", "category_id": "cat3"}
        ]
    return []

@app.post("/api/prompts")
def create_prompt(prompt_data: dict):
    user_prompt = prompt_data.get("prompt", "")
    response = f"""# Lesson: {user_prompt}

This is a comprehensive lesson about your question: "{user_prompt}"

## Introduction
Welcome to this educational lesson. This topic is fascinating and has many practical applications in the real world.

## Key Concepts
1. **Understanding the Basics**: Let's start with the fundamental concepts
2. **Real-world Applications**: How this applies to everyday life
3. **Advanced Considerations**: Deeper insights for further learning

## Examples
- Example 1: Practical demonstration
- Example 2: Case study analysis
- Example 3: Interactive scenario

## Summary
This lesson covered the essential aspects of {user_prompt}. Continue exploring this topic to deepen your understanding.

## Next Steps
- Practice what you've learned
- Explore related topics
- Apply knowledge in real situations
"""
    
    return {
        "id": "prompt123",
        "response": response,
        "message": "Lesson generated successfully"
    }

@app.get("/api/users/{user_id}/prompts")
def get_user_prompts(user_id: str):
    return [
        {
            "id": "prompt1",
            "prompt": "Teach me about black holes",
            "response": "Black holes are fascinating cosmic objects...",
            "created_at": "2024-01-15T10:30:00Z"
        },
        {
            "id": "prompt2",
            "prompt": "Explain quantum physics",
            "response": "Quantum physics is the study of matter and energy...",
            "created_at": "2024-01-14T15:20:00Z"
        }
    ]

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)