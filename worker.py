import os
from rq import Worker, Queue, Connection
from app.utils.redis_client import redis_client
from app.core import tasks
from loguru import logger

if __name__ == "__main__":
    # Pass the Redis client directly (RQ handles the pool internally)
    with Connection(redis_client):
        worker = Worker(Queue("llm_tasks"))
        logger.info("🚀 RQ Worker started. Waiting for jobs...")
        logger.info("   Press CTRL+C to stop.")
        worker.work()