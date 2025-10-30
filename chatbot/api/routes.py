# chatbot/api/routes.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from chatbot.api.schemas import ProjectCreate, ProjectRead
from chatbot.core.database import get_db
from chatbot.core.models import Project

router = APIRouter(prefix="/api", tags=["projects"])


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