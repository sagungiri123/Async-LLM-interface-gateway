import pytest
from pydantic import ValidationError
from app.models.schemas import GenerateRequest, TaskResponse


class TestGenerateRequest:
    def test_valid_request(self):
        req = GenerateRequest(prompt="Hello AI", max_length=50)
        assert req.prompt == "Hello AI"
        assert req.max_length == 50

    def test_default_max_length(self):
        req = GenerateRequest(prompt="Hello")
        assert req.max_length == 50

    def test_prompt_must_be_string(self):
        with pytest.raises(ValidationError):
            GenerateRequest(prompt=12345)

    def test_max_length_must_be_integer(self):
        with pytest.raises(ValidationError):
            GenerateRequest(prompt="Hello", max_length="not-a-number")

    def test_missing_prompt_raises(self):
        with pytest.raises(ValidationError):
            GenerateRequest(max_length=50)


class TestTaskResponse:
    def test_minimal_response(self):
        resp = TaskResponse(task_id="abc-123", status="queued")
        assert resp.task_id == "abc-123"
        assert resp.status == "queued"
        assert resp.result is None
        assert resp.error is None

    def test_full_response(self):
        resp = TaskResponse(
            task_id="abc-123",
            status="finished",
            result={"generated_text": "Hello world"},
        )
        assert resp.result["generated_text"] == "Hello world"