class TestHealthEndpoint:
    def test_health_returns_200(self, client):
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"


class TestGenerateEndpoint:
    def test_generate_returns_202_with_task_id(self, client, mock_queue):
        response = client.post(
            "/generate",
            json={"prompt": "Hello AI", "max_length": 50},
        )
        assert response.status_code == 202
        data = response.json()
        assert data["task_id"] == "test-task-id-12345"
        assert data["status"] == "queued"

    def test_generate_enqueues_task(self, client, mock_queue):
        client.post("/generate", json={"prompt": "Test prompt"})
        assert mock_queue.enqueue.call_count == 1

    def test_generate_rejects_invalid_prompt_type(self, client):
        response = client.post("/generate", json={"prompt": 12345})
        assert response.status_code == 422

    def test_generate_rejects_missing_prompt(self, client):
        response = client.post("/generate", json={"max_length": 50})
        assert response.status_code == 422

    def test_generate_accepts_optional_max_length(self, client, mock_queue):
        response = client.post("/generate", json={"prompt": "Hi"})
        assert response.status_code == 202


class TestResultEndpoint:
    def test_result_not_found_returns_404(self, client):
        response = client.get("/result/does-not-exist")
        assert response.status_code == 404