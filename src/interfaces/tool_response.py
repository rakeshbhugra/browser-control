from pydantic import BaseModel

class ToolResponse(BaseModel):
    text_response: str
    tool_output: str
