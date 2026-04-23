import sys
from unittest.mock import MagicMock
from fastapi.testclient import TestClient

# Mock the entire redis module before importing the app, so that when main.py imports redis, it gets our mock instead of the real module
mock_redis_module = MagicMock()
sys.modules['redis'] = mock_redis_module

# Configure the fake module so that calling redis.Redis() returns our specific mock
mock_redis_instance = MagicMock()
mock_redis_module.Redis.return_value = mock_redis_instance

from main import app 

# Create a test client for the FastAPI app
def test_create_job_success():
    # Clear any previous mock calls
    mock_redis_instance.reset_mock()
    
    client = TestClient(app)
    response = client.post("/jobs")
    
    assert response.status_code == 200
    data = response.json()
    assert "job_id" in data
    
    # Verify our mocked Redis was actually called by the API
    mock_redis_instance.lpush.assert_called_once()
    mock_redis_instance.hset.assert_called_once()

def test_get_job_success():
    mock_redis_instance.reset_mock()
    
    # Mocked Redis returning a status for the job
    mock_redis_instance.hget.return_value = b"completed"
    
    client = TestClient(app)
    response = client.get("/jobs/123e4567-e89b-12d3-a456-426614174000")
    
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "completed"
    assert data["job_id"] == "123e4567-e89b-12d3-a456-426614174000"

def test_get_job_not_found():
    mock_redis_instance.reset_mock()
    
    # Mocked Redis returning None (job doesn't exist)
    mock_redis_instance.hget.return_value = None
    
    client = TestClient(app)
    response = client.get("/jobs/nonfound-job")
    
    # FastAPI HTTPException returns a 404 status code
    assert response.status_code == 404
    data = response.json()
    assert "detail" in data