from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from routes import users, categories, sub_categories, prompts
import traceback

app = FastAPI(
    title="AI Learning Platform API",
    description="API for AI-driven learning platform",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error", "error": str(exc)}
    )


app.include_router(users.router, prefix="/api", tags=["users"])
app.include_router(categories.router, prefix="/api", tags=["categories"])
app.include_router(sub_categories.router, prefix="/api", tags=["sub-categories"])
app.include_router(prompts.router, prefix="/api", tags=["prompts"])

@app.get("/")
def read_root():
    return {"message": "Welcome to AI Learning Platform API"}

@app.get("/health")
def health_check():
    return {"status": "healthy", "message": "API is running"}