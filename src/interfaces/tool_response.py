from pydantic import BaseModel

class ToolResponse(BaseModel):
    text_response: str
    tool_output: str
    tool_worked: bool
