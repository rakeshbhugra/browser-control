from src.interfaces.events import Event, FunctionDetails
from src.sqlite_manager.setup_sql import SessionLocal
from typing import List
from src.sqlite_manager.create_events_db import EventsDB
from datetime import datetime

async def get_previous_events(user_id: str) -> List[Event]:
    session = SessionLocal()
    events_db = session.query(EventsDB).filter(EventsDB.user_id == user_id).all()
    
    # Convert EventsDB objects to Event objects
    events = []
    for event_db in events_db:
        # Create FunctionDetails object
        function_details = FunctionDetails(
            name=event_db.function_name,
            args=event_db.function_args,
            response=event_db.function_response
        )
        
        # Create Event object
        event = Event(
            user_id=event_db.user_id,
            role=event_db.role,
            content=event_db.content,
            message_type=event_db.message_type,
            function_details=function_details,
            event_timestamp=event_db.event_timestamp
        )
        events.append(event)
        
    session.close()
    return events
