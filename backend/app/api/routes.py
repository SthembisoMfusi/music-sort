from fastapi import APIRouter, HTTPException, Query, Depends
from typing import List, Optional
from pydantic import BaseModel
from ..services.extractor import MediaExtractorService


router = APIRouter(prefix="/api/v1", tags=["Media Engine"])

def get_extractor():
    return MediaExtractorService()

class SearchResult(BaseModel):
    id: Optional[str]
    title: str
    artists: List[str]
    album: Optional[str]
    duration: Optional[str]
    thumbnail: List[dict]
    type: Optional[str]

class StreamResponse(BaseModel):
    video_id: str
    mode: str
    stream_url: str


class DownloadRequest(BaseModel):
    video_id: str
    mode: Optional[str] = "audio" # audio or video

class TaskResponse(BaseModel):
    task_id: str
    status: str

@router.get("/stream/{video_id}", response_model=StreamResponse)
async def get_stream(video_id: str,
                     mode: str = Query("audio", description="Options: audio, video"),
                     extractor: MediaExtractorService = Depends(get_extractor)):
    """
    Get stream URL for a given video ID.

    Args:
        video_id (str): The YouTube video ID
        mode (str): The mode of extraction (audio or video)
        extractor (MediaExtractorService): The media extractor service

    Returns:
        StreamResponse: The stream URL response
    """
    try:
        stream_url = await extractor.get_stream_url(video_id, mode)
        if not stream_url:
            raise HTTPException(status_code=404, detail="Could not extract stream URL")
        return StreamResponse(video_id=video_id, mode=mode, stream_url=stream_url)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))





# --- Endpoints ---

@router.post("/download", response_model=TaskResponse, status_code=202)
async def trigger_download(payload: DownloadRequest):
    """
    Asynchronously queue a download job. Returns instantly with a task ID.
    """
    # Fire and forget into the Redis queue via Celery delay()
    task = download_media.delay(payload.video_id, payload.mode)
    return {"task_id": task.id, "status": "QUEUED"}

@router.get("/download/status/{task_id}")
async def get_download_status(task_id: str):
    """
    Poll the active progress, state, and percentage telemetry of a download task.
    """
    task_result = AsyncResult(task_id)

    response = {
        "task_id": task_id,
        "state": task_result.state,
    }

    if task_result.state == 'PROGRESS':
        response["meta"] = task_result.info
    elif task_result.state == 'SUCCESS':
        response["result"] = task_result.result 
    elif task_result.state == 'FAILURE':
        response["error"] = str(task_result.info)

    return response