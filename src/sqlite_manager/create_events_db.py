from sqlalchemy import Column, String, DateTime
from src.sqlite_manager.setup_sql import engine, Base
from src.interfaces.events import Event

class EventsDB(Base):
    __tablename__ = "events"
    user_id = Column(String, primary_key=True)
    role = Column(String)
    content = Column(String)
    message_type = Column(String)
    function_name = Column(String)
    function_args = Column(String)
    function_response = Column(String)
    event_timestamp = Column(DateTime)

def create_events_db():
    Base.metadata.create_all(bind=engine)
