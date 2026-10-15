import pytest
from httpx import AsyncClient
import time
from app.main import app

BASE_URL = "http://test"

@pytest.mark.asyncio
async def test_root_endpoint():
    """Verifies that the central gateway is online and functional."""
    async with AsyncClient(app=app, base_url=BASE_URL) as ac:
        response = await ac.get("/")
    assert response.status_code == 200
    assert response.json()["status"] == "online"

@pytest.mark.asyncio
async def test_search_endpoint():
    """Verifies that the ytmusicapi scraper extracts structured search results."""
    async with AsyncClient(app=app, base_url=BASE_URL) as ac:
        response = await ac.get("/api/search", params={"q": "Blinding Lights", "filter_type": "songs"})

    assert response.status_code == 200
    results = response.json()
    assert isinstance(results, list)
    if len(results) > 0:
        first_item = results[0]
        assert "id" in first_item
        assert "title" in first_item
        assert "artists" in first_item

@pytest.mark.asyncio
async def test_stream_extraction():
    """Verifies that yt-dlp correctly resolves an ad-free googlevideo stream URL."""
    test_video_id = "jNQXAC9IVRw"  # Short test ID
    async with AsyncClient(app=app, base_url=BASE_URL) as ac:
        response = await ac.get(f"/api/stream/{test_video_id}", params={"mode": "audio"})

    assert response.status_code == 200
    data = response.json()
    assert data["video_id"] == test_video_id
    assert "stream_url" in data
    assert "googlevideo.com" in data["stream_url"]

@pytest.mark.asyncio
async def test_download_pipeline_trigger():
    """Verifies that the download route pushes tasks into the Celery/Redis queue topology."""
    test_video_id = "jNQXAC9IVRw"
    async with AsyncClient(app=app, base_url=BASE_URL) as ac:
        # Trigger async download task
        trigger_response = await ac.post("/api/download", json={"video_id": test_video_id, "mode": "audio"})
        assert trigger_response.status_code == 202

        trigger_data = trigger_response.json()
        assert "task_id" in trigger_data
        assert trigger_data["status"] == "QUEUED"

        # Immediately poll status endpoint to check contract binding
        task_id = trigger_data["task_id"]
        status_response = await ac.get(f"/api/download/status/{task_id}")
        assert status_response.status_code == 200
        assert "state" in status_response.json()
