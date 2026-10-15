from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import router as media_router

app = FastAPI(
    title="YouTube Music Nexus API",
    description="Asynchronous Media Extraction & Queue Backend Engine for Personal Use",
    version="1.0.0"
)

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
        "engine": "FastAPI + Celery Worker Active",
        "documentation": "/docs"
    }
