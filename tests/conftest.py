import pytest
from unittest.mock import MagicMock, patch

@pytest.fixture(scope="session", autouse=True)
def patch_redis():
    
    with patch("app.utils.redis_client.redis_client") as mock_redis, \
        patch("rq.Queue") as mock_queue_class:
            mock_redis.connection_pool = MagicMock()
            
            # Queue() returns a MagicMock instance
            
            yield mock_redis
            
@pytest.fixture
def client():
    from app.main import app
    from fastapi.testclient import TestClient
    return TestClient(app)

@pytest.fixture
def mock_queue():
    
    with patch("app.main.queue") as mock_q:
        fake_job = MagicMock()
        fake_job.id = "test-task-id-12345"
        mock_q.enqueue.return_value = fake_job
        yield mock_q
        
  