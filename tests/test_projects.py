import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import sessionmaker

from chatbot.main import app
from chatbot.core.database import Base, get_db
from chatbot.core import models  # WICHTIG: importiere Models VOR dem Erstellen der Tabellen

# === Test-Datenbank (Persistente SQLite) ===
SQLALCHEMY_DATABASE_URL = "sqlite:////Users/luiswohner/Documents/GitHub/Chatty/chatty.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)


# === Dependency Override für FastAPI ===
def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)


@pytest.fixture(scope="module", autouse=True)
def setup_database():
    """Erstellt die Tabellen vor den Tests."""
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)  # Aufräumen nach den Tests


def ensure_projects_table():
    """Prüft, ob die Tabelle `projects` existiert, und erstellt sie bei Bedarf."""
    inspector = inspect(engine)
    if "projects" not in inspector.get_table_names():
        Base.metadata.create_all(bind=engine)


# === Tests ===
def test_create_project():
    ensure_projects_table()  # Sicherstellen, dass die Tabelle existiert
    payload = {"name": "Testprojekt", "description": "Ein Test"}
    resp = client.post("/api/projects", json=payload)
    assert resp.status_code == 201, resp.text  # Erwartet 201 für erfolgreich erstellte Ressourcen
    data = resp.json()
    assert data["name"] == "Testprojekt"
    assert data["description"] == "Ein Test"
    assert "id" in data
    assert "created_at" in data


def test_get_projects():
    ensure_projects_table()  # Sicherstellen, dass die Tabelle existiert
    # Erst ein Projekt erstellen
    client.post("/api/projects", json={"name": "Projekt 1", "description": "ABC"})
    # Dann abrufen
    resp = client.get("/api/projects")
    assert resp.status_code == 200, resp.text
    projects = resp.json()
    assert isinstance(projects, list)
    assert len(projects) > 0