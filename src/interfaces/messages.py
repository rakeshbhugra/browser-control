from pydantic import BaseModel
from typing import List

class FunctionDetails(BaseModel):
    name: str
    args: dict
    response: str

class Message(BaseModel):
    role: str
    content: str
    message_type: str
    function_details: FunctionDetails

class Messages(BaseModel):
    messages: List[Message]
