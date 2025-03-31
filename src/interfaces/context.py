from pydantic import BaseModel
from playwright.async_api import Page
from typing import Optional, Dict

class Context(BaseModel):
    user_id: str
    page: Optional[Page] = None
    element_index_dict: Optional[Dict] = None
    messages_for_llm: str
    plan: Optional[str] = None
