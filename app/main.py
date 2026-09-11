from fastapi import FastAPI, HTTPException
from rq import Queue
from rq.job import Job
from app.models.schemas import GenerateRequest, TaskResponse
from app.utils.redis_client import redis_client
from app.core.tasks import generate_text_task

app = FastAPI(title="Async LLM API")

# Pass the Redis client directly to Queue (not connection_pool)
queue = Queue("llm_tasks", connection=redis_client)


@app.get("/health")
async def health_check():
    return {"status": "healthy", "message": "FastAPI is running!"}


@app.post("/generate", response_model=TaskResponse, status_code=202)
async def generate(request: GenerateRequest):
    job = queue.enqueue(
        generate_text_task,
        request.prompt,
        request.max_length,
        job_timeout=300,
        result_ttl=3600
    )
    print(f"📦 Enqueued job {job.id}")
    return TaskResponse(task_id=job.id, status="queued")


@app.get("/result/{task_id}", response_model=TaskResponse)
async def get_result(task_id: str):
    try:
        job = Job.fetch(task_id, connection=redis_client)
    except Exception:
        raise HTTPException(status_code=404, detail="Task ID not found")

    if job.is_finished:
        return TaskResponse(task_id=task_id, status="finished", result=job.return_value())
    elif job.is_queued:
        return TaskResponse(task_id=task_id, status="queued")
    elif job.is_started:
        return TaskResponse(task_id=task_id, status="processing")
    elif job.is_failed:
        return TaskResponse(task_id=task_id, status="failed", error=str(job.exc_info))
    else:
        return TaskResponse(task_id=task_id, status="unknown")