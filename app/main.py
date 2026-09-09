from fastapi import FastAPI
from rq import Queue
from app.models.schemas import GenerateRequest, TaskResponse
from app.utils.redis_client import redis_client
from app.core.tasks import generate_text_task
import uuid

app = FastAPI(title="Async LLM API")

# Initialize the RQ Queue. It connects to Redis using our redis_client.
queue = Queue("llm_tasks", connection=redis_client)

@app.get("/health")
async def health_check():
    return {"status": "healthy", "message": "FastAPI is running!"}

@app.post("/generate", response_model=TaskResponse, status_code=202)
async def generate(request: GenerateRequest):
   
    
    job = queue.enqueue(
        generate_text_task,        # The function to run in the background
        request.prompt,            # Argument 1
        request.max_length,        # Argument 2
        job_timeout=300,           # If the job runs longer than 5 minutes, mark as failed
        result_ttl=3600            # Keep the result in Redis for 1 hour
    )

    print(f"📦 Enqueued job {job.id} with prompt: {request.prompt[:30]}...")

    return TaskResponse(
        task_id=job.id,
        status="queued"
    )

