from pydantic import BaseModel
from typing import List
class Message(BaseModel):
    role: str
    content: str
    function_name: str
    function_args: str

class Messages(BaseModel):
    messages: List[Message]
