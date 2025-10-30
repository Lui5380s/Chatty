import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from chatbot.main import app
from chatbot.core.database import Base, get_db
from chatbot.core import models  # WICHTIG: importiere Models VOR dem Erstellen der Tabellen

# === Test-Datenbank (In-Memory SQLite) ===
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

# === Tabellen erstellen ===
Base.metadata.create_all(bind=engine)


# === Dependency Override für FastAPI ===
def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)


# === Tests ===
def test_create_project():
    payload = {"name": "Testprojekt", "description": "Ein Test"}
    resp = client.post("/api/projects", json=payload)
    assert resp.status_code == 200, resp.text
    data = resp.json()
    assert data["name"] == "Testprojekt"
    assert "id" in data


def test_get_projects():
    # Erst ein Projekt erstellen
    client.post("/api/projects", json={"name": "Projekt 1", "description": "ABC"})
    # Dann abrufen
    resp = client.get("/api/projects")
    assert resp.status_code == 200, resp.text
    projects = resp.json()
    assert isinstance(projects, list)
    assert len(projects) > 0