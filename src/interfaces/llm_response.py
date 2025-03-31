from pydantic import BaseModel
from typing import Optional

class LLMResponse(BaseModel):
    function_name: Optional[str] = None
    function_args: Optional[dict] = None
    text: Optional[str] = None
