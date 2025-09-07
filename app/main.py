from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import users, categories,prompts

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


app.include_router(users.router, prefix="/api", tags=["users"])
app.include_router(categories.router, prefix="/api", tags=["categories"])
app.include_router(prompts.router, prefix="/api", tags=["prompts"])

@app.get("/")
def read_root():
    return {"message": "Welcome to AI Learning Platform API"}