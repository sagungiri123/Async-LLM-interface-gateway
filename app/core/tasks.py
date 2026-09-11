import os
import time

from rq import get_current_job
from loguru import logger

# Global variables to hold the model in memory
_model = None
_tokenizer = None

def load_model():
    """
    Lazy loads the HuggingFace model into memory.
    Only runs the first time a job is processed.
    """
    global _model, _tokenizer

    if _model is None:
        logger.info(" Loading AI model 'distilgpt2'... (this may take a moment)")
        
        # Import torch HERE (only runs inside the worker)
        import torch
        from transformers import AutoModelForCausalLM, AutoTokenizer

        model_name = "distilgpt2"
        _tokenizer = AutoTokenizer.from_pretrained(model_name)
        _model = AutoModelForCausalLM.from_pretrained(model_name)
        _tokenizer.pad_token = _tokenizer.eos_token

        logger.success(" Model loaded into memory. Ready for inference.")

    return _model, _tokenizer
    
def generate_text_task(prompt: str, max_length: int = 50):
    
    import torch
   
    job = get_current_job()
    job_id = job.id if job else "unknown"

    logger.info(f" Worker started Job {job_id}")
    logger.info(f"   Prompt: '{prompt[:40]}...' (max_length: {max_length})")

    start_time = time.time()
    
    # 1, load the model 
    model, tokenizer = load_model()
    
    # 2. tokenize the input (convert text to numbers)
    inputs = tokenizer(prompt, return_tensors="pt")
    
    # 3. Generate the output
    # -> This line tells "PyTorch", that: We are only doing prediction, not training.
    #    Don't waste memory tracking gradients. This saves 50% memory usase.
    with torch.no_grad():
        outputs = model.generate(
            inputs.input_ids,
            max_length = max_length,
            do_sample=True,
            temperature=0.8,
            top_p = 0.95,
            pad_token_id = tokenizer.eos_token_id
        )
        
    # 4. Decode the numbers back into human-readable text
    generated_text = tokenizer.decode(outputs[0], skip_special_tokens=True)
    
    
    duration = time.time() - start_time
    logger.success(f" Job {job_id} finished in {duration:.2f} seconds")
    logger.info(f"Generated: {generated_text[:80]}...")
    

    # Return a dictionary. RQ will store this in Redis under the job ID.
    return {
        "prompt": prompt,
        "generated_text": generated_text,
        "inference_time_seconds": round(duration, 2),
        "model": "distilgpt2"
    }