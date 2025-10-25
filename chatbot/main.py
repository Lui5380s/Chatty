# chatbot/main.py
from fastapi import FastAPI
from chatbot.api.routes import router as api_router
from chatbot.core.database import init_db
from chatbot.config import settings

app = FastAPI(title=settings.project_name)

@app.on_event("startup")
def on_startup():
    init_db()

app.include_router(api_router, prefix="/api")

@app.get("/")
def root():
    return {"message": f"Welcome to {settings.project_name}!"}