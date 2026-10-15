import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app

BASE_URL = "http://test"
# Global stable music video ID for testing format extraction pipelines
VALID_TEST_ID = "dQw4w9WgXcQ"

@pytest.mark.asyncio
async def test_root_endpoint():
    """Verifies that the central gateway is online and functional."""
    async with AsyncClient(transport=ASGITransport(app=app), base_url=BASE_URL) as ac:
        response = await ac.get("/")
    assert response.status_code == 200
    assert response.json()["status"] == "online"

@pytest.mark.asyncio
async def test_search_endpoint():
    """Verifies that the ytmusicapi scraper extracts structured search results."""
    async with AsyncClient(transport=ASGITransport(app=app), base_url=BASE_URL) as ac:
        response = await ac.get("/api/v1/search", params={"q": "Blinding Lights", "filter_type": "songs"})

    assert response.status_code == 200
    results = response.json()
    assert isinstance(results, list)

@pytest.mark.asyncio
async def test_stream_extraction():
    """Verifies that yt-dlp correctly resolves an ad-free googlevideo stream URL."""
    async with AsyncClient(transport=ASGITransport(app=app), base_url=BASE_URL) as ac:
        response = await ac.get(f"/api/v1/stream/{VALID_TEST_ID}?mode=audio")

    assert response.status_code == 200
    data = response.json()
    assert data["video_id"] == VALID_TEST_ID
    assert "googlevideo.com" in data["stream_url"]

@pytest.mark.asyncio
async def test_download_pipeline_trigger():
    """Verifies that the download route pushes tasks into the Celery/Redis queue topology."""
    async with AsyncClient(transport=ASGITransport(app=app), base_url=BASE_URL) as ac:
        trigger_response = await ac.post("/api/v1/download", json={"video_id": VALID_TEST_ID, "mode": "audio"})
        assert trigger_response.status_code == 202

        trigger_data = trigger_response.json()
        assert "task_id" in trigger_data

        task_id = trigger_data["task_id"]
        status_response = await ac.get(f"/api/v1/download/status/{task_id}")
        assert status_response.status_code == 200
