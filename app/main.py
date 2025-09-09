from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from routes import users, categories, sub_categories, prompts
import traceback
import os

app = FastAPI(
    title="AI Learning Platform API",
    description="API for AI-driven learning platform",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000", "*"],  # Allow React dev server
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

@app.middleware("http")
async def log_requests(request: Request, call_next):
    """Log all incoming requests for debugging"""
    print(f"Incoming request: {request.method} {request.url}")
    print(f"Headers: {dict(request.headers)}")
    
    response = await call_next(request)
    print(f"Response status: {response.status_code}")
    
    return response

@app.middleware("http")
async def add_cors_headers(request: Request, call_next):
    """Add CORS headers to all responses"""
    response = await call_next(request)

    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE, OPTIONS"
    response.headers["Access-Control-Allow-Headers"] = "*"
    response.headers["Access-Control-Allow-Credentials"] = "true"
    
    return response

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    print(f"Global Exception: {exc}")
    print(f"Request: {request.method} {request.url}")
    print(f"Traceback: {traceback.format_exc()}")
    
    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "error": "Internal server error",
            "detail": str(exc),
            "path": str(request.url)
        }
    )

@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    print(f"HTTP Exception: {exc.detail}")
    print(f"Request: {request.method} {request.url}")
    
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success": False,
            "error": exc.detail,
            "status_code": exc.status_code,
            "path": str(request.url)
        }
    )

app.include_router(users.router, prefix="/api", tags=["users"])
app.include_router(categories.router, prefix="/api", tags=["categories"])
app.include_router(sub_categories.router, prefix="/api", tags=["sub-categories"])
app.include_router(prompts.router, prefix="/api", tags=["prompts"])

@app.get("/")
def read_root():
    return {
        "message": "Welcome to AI Learning Platform API",
        "version": "1.0.0",
        "docs": "/docs",
        "status": "running",
        "available_endpoints": {
            "users_register": "POST /api/users/register",
            "users_login": "POST /api/users/login",
            "users_list": "GET /api/users",
            "categories": "GET /api/categories",
            "health": "GET /health"
        }
    }

@app.get("/health")
def health_check():
    try:
        from config import db
        db.command('ping')
        db_status = "connected"
    except Exception as e:
        db_status = f"error: {str(e)}"
    
    return {
        "status": "healthy",
        "message": "API is running",
        "database": db_status,
        "openai": "configured" if os.getenv("OPENAI_API_KEY") else "not configured"
    }

@app.options("/{full_path:path}")
async def options_handler(request: Request):
    return JSONResponse(
        status_code=200,
        content={"message": "OK"},
        headers={
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "GET, POST, PUT, DELETE, OPTIONS",
            "Access-Control-Allow-Headers": "*",
        }
    )

@app.get("/api/test")
def test_endpoint():
    return {"message": "API is working", "status": "success"}

@app.post("/api/test")
def test_post_endpoint():
    return {"message": "POST method working", "status": "success"}

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    host = os.getenv("HOST", "0.0.0.0")
    
    print(f"Starting AI Learning Platform API on {host}:{port}")
    print(f"Available at: http://localhost:{port}")
    print(f"API Documentation: http://localhost:{port}/docs")
    
    uvicorn.run(app, host=host, port=port, reload=True)