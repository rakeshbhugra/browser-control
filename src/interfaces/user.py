from pydantic import BaseModel
from src.interfaces.messages import Messages

class User(BaseModel):
    # user_id: str
    messages: Messages
