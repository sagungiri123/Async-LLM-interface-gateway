import os
from rq import Worker, Queue
from app.utils.redis_client import redis_client
from app.core import tasks
from loguru import logger

if __name__ == "__main__":
    
    # connect to redis using our connection pool

    # Create a queue bound to our redis connection and start a worker
    queue = Queue("llm_tasks", connection=redis_client)
    worker = Worker([queue], connection=redis_client)
    logger.info("RQ worker started. waiting for jobs..")
    logger.info("press CTRL+C to stop.")
    worker.work()  # This starts an infinite loop, polling redis for jobs