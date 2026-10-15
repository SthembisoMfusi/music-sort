from fastapi import APIRouter, HTTPException, Query, Depends
from typing import List, Optional, Any
from pydantic import BaseModel, Field
from app.services.extractor import MediaExtractorService

router = APIRouter(prefix="/api/v1", tags=["Media Engine"])

def get_extractor():
    return MediaExtractorService()

# --- Upgraded, Flexible Data Contracts ---
class SearchResult(BaseModel):
    id: Optional[str] = None
    title: Optional[str] = "Unknown Title"
    artists: Optional[List[Any]] = Field(default_factory=list)  # Allows strings or nested objects safely
    album: Optional[Any] = None
    duration: Optional[str] = None
    thumbnail: Optional[str] = None
    type: Optional[str] = None

class StreamResponse(BaseModel):
    video_id: str
    mode: str
    stream_url: str

class DownloadRequest(BaseModel):
    video_id: str
    mode: Optional[str] = "audio"

class TaskResponse(BaseModel):
    task_id: str
    status: str

# --- HTTP Route Layouts ---

@router.get("/search", response_model=List[SearchResult])
async def search(
        q: str = Query(..., description="The search query text"),
        filter_type: str = Query("songs", description="Options: songs, videos, albums"),
        extractor: MediaExtractorService = Depends(get_extractor)
):
    """Search YouTube Music securely and return structured metadata."""
    if not q.strip():
        raise HTTPException(status_code=400, detail="Search query cannot be empty")
    results = await extractor.search_music(q, filter_type=filter_type)
    return results

@router.get("/stream/{video_id}", response_model=StreamResponse)
async def get_stream(
        video_id: str,
        mode: str = Query("audio", description="Options: audio, video"),
        extractor: MediaExtractorService = Depends(get_extractor)
):
    """Resolve a fresh, ad-free streaming URL on-demand."""
    stream_url = await extractor.get_stream_url(video_id, mode=mode)
    if not stream_url:
        raise HTTPException(status_code=404, detail="Could not extract stream link.")
    return {"video_id": video_id, "mode": mode, "stream_url": stream_url}

# Add our missing POST download task registration wrapper directly onto our clean router instance
from app.workers.tasks import download_media
from celery.result import AsyncResult

@router.post("/download", response_model=TaskResponse, status_code=202)
async def trigger_download(payload: DownloadRequest):
    """Asynchronously queue a download job."""
    task = download_media.delay(payload.video_id, payload.mode)
    return {"task_id": task.id, "status": "QUEUED"}

@router.get("/download/status/{task_id}")
async def get_download_status(task_id: str):
    """Poll active progress telemetry."""
    task_result = AsyncResult(task_id)
    response = {"task_id": task_id, "state": task_result.state}
    if task_result.state == 'PROGRESS':
        response["meta"] = task_result.info
    elif task_result.state == 'SUCCESS':
        response["result"] = task_result.result
    elif task_result.state == 'FAILURE':
        response["error"] = str(task_result.info)
    return response
