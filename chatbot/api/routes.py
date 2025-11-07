# chatbot/api/routes.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from passlib.context import CryptContext
from datetime import timedelta, datetime
from jose import jwt, JWTError

from chatbot.api.schemas import ProjectCreate, ProjectRead, ChatRequest, ChatResponse, UserCreate, UserRead
from chatbot.core.database import get_db
from chatbot.core.models import Project, User
import os

router = APIRouter(prefix="/api", tags=["projects"])

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

SECRET_KEY = os.environ.get("SECRET_KEY", "your_secret_key")  # Fallback für Entwicklung
ALGORITHM = os.environ.get("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.environ.get("ACCESS_TOKEN_EXPIRE_MINUTES", 30))


# Hilfsfunktion zum Erstellen eines Tokens
def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


@router.get("/projects", response_model=List[ProjectRead])
def get_projects(db: Session = Depends(get_db)):
    """Alle Projekte abrufen"""
    projects = db.query(Project).all()
    return projects


@router.get("/projects/{project_id}", response_model=ProjectRead)
def get_project(project_id: int, db: Session = Depends(get_db)):
    """Ein einzelnes Projekt anhand der ID abrufen"""
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Projekt nicht gefunden")
    return project


@router.post("/projects", response_model=ProjectRead, status_code=201)
def create_project(project: ProjectCreate, db: Session = Depends(get_db)):
    """Neues Projekt erstellen"""
    new_project = Project(name=project.name, description=project.description)
    db.add(new_project)
    db.commit()
    db.refresh(new_project)
    return new_project


@router.post("/chat", response_model=ChatResponse)
def chat_endpoint(chat_request: ChatRequest):
    """Chatbot-Nachricht verarbeiten."""
    if not chat_request.message:
        raise HTTPException(status_code=422, detail="Nachricht darf nicht leer sein.")

    # Beispielantwort generieren
    response = ChatResponse(
        user_input=chat_request.message,
        chatty_response=f"Antwort auf: {chat_request.message}",
        project=chat_request.project
    )
    return response


@router.post("/register", response_model=UserRead, status_code=201)
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    """Registriert einen neuen Benutzer."""
    password = user.password[:72]  # Passwort explizit kürzen
    hashed_password = pwd_context.hash(password)
    new_user = User(
        username=user.username,
        email=user.email,
        hashed_password=hashed_password
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.post("/login")
def login_user(username: str, password: str, db: Session = Depends(get_db)):
    """Benutzer-Login."""
    user = db.query(User).filter(User.username == username).first()
    if not user or not pwd_context.verify(password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Ungültige Anmeldedaten")

    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}