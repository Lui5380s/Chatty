from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from chatbot.config import settings
import os

# SQLite Pfad
DB_URL = f"sqlite:///{os.path.join(os.getcwd(), 'chatty.db')}"

# Engine & Session
engine = create_engine(DB_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

# Base-Klasse für alle Models
Base = declarative_base()


def init_db():
    """Erstellt alle Tabellen, falls sie noch nicht existieren."""
    from chatbot.core import models  # wichtig, damit SQLAlchemy die Klassen kennt
    Base.metadata.create_all(bind=engine)

def get_db():
    """Dependency, um eine DB-Session bereitzustellen (für FastAPI Depends)."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()