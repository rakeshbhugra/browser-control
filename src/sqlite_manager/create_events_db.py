from sqlalchemy import Column, String, DateTime, Integer
from src.sqlite_manager.setup_sql import engine, Base
from src.interfaces.events import Event

class EventsDB(Base):
    __tablename__ = "events"
    event_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(String, index=True)
    role = Column(String)
    content = Column(String)
    message_type = Column(String)
    function_name = Column(String)
    function_args = Column(String)
    function_response = Column(String)
    event_timestamp = Column(DateTime)

def create_events_db():
    Base.metadata.create_all(bind=engine)
