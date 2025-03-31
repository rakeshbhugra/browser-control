from src.interfaces.events import Event
from src.sqlite_manager.setup_sql import SessionLocal
from typing import List

async def get_previous_events(user_id: str) -> List[Event]:
    session = SessionLocal()
    events = session.query(Event).filter(Event.user_id == user_id).all()
    session.close()
    return events
