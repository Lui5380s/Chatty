# chatbot/core/db.py
from sqlmodel import SQLModel, create_engine, Session
from chatbot.config import settings

engine = create_engine(settings.database_url, echo=settings.debug)

def init_db():
    """Initialisiert alle Tabellen (wird später von main.py aufgerufen)."""
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session