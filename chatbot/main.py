# chatbot/main.py
from fastapi import FastAPI
from chatbot.core.database import init_db
from chatbot.api.routes import router as project_router  # <--- hier

app = FastAPI(title="Chatty API")

# Routen registrieren
app.include_router(project_router)

# DB initialisieren
@app.on_event("startup")
def on_startup():
    init_db()