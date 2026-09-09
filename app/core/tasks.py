import time
from rq import get_current_job
from loguru import logger

def generate_text_task(prompt: str, max_length: int = 50):
   
    job = get_current_job()
    job_id = job.id if job else "unknown"

    logger.info(f"🟡 Worker started Job {job_id}")
    logger.info(f"   Prompt: '{prompt[:30]}...' (max_length: {max_length})")


    start_time = time.time()
    time.sleep(5)  # Simulate 5 seconds of "thinking"

    generated_text = f"AI generated response to: '{prompt}' (simulated, max_length={max_length})"

    duration = time.time() - start_time
    logger.success(f"✅ Job {job_id} finished in {duration:.2f} seconds")

    # Return a dictionary. RQ will store this in Redis under the job ID.
    return {
        "prompt": prompt,
        "generated_text": generated_text,
        "inference_time_seconds": round(duration, 2)
    }