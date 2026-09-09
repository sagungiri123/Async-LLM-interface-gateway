from pydantic import BaseModel
from typing import Optional, Dict, Any

class GenerateRequest(BaseModel):
    prompt: str
    max_length: Optional[int] = 50 
    
    
class TaskResponse(BaseModel):
    task_id: str
    status: str
    result: Optional[Dict[str, Any]] = None
    error: Optional[str] = None