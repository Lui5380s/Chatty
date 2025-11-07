# chatbot/main.py
from fastapi import FastAPI
from fastapi import FastAPI
from contextlib import asynccontextmanager
from chatbot.core.database import init_db
from chatbot.api.routes import router as project_router  # <--- hier

@asynccontextmanager
def lifespan(app: FastAPI):
    """Lifespan-Event-Handler für Startup und Shutdown."""
    init_db()  # Startup-Logik
    yield
    # Shutdown-Logik (falls erforderlich)

app = FastAPI(title="Chatty API", lifespan=lifespan)

# Routen registrieren
app.include_router(project_router)