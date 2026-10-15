from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import router as media_router

app = FastAPI(
    title= "YouTube Music Nexus API",
    description
    = "An API for extracting audio from YouTube videos",
    version="1.0.0"

)

# cors configuration

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(media_router)
@app.get("/")
async def root():
    return {
        "status": "online",
        "engine": "FastApi + Celery worker active",
        "message": "Welcome to the YouTube Music Nexus API",
        "documentation": "/docs"
    }
