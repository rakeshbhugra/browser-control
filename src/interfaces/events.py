from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class FunctionDetails(BaseModel):
    name: str
    args: dict
    response: str

class Event(BaseModel):
    '''
    TODO: we should have session_id for same user's multiple sessions but ok for now
    '''
    user_id: str
    role: str
    content: str
    message_type: str
    function_details: Optional[FunctionDetails] = None
    event_timestamp: datetime

class Events(BaseModel):
    events: List[Event]
