import pytest
from fastapi.testclient import TestClient
from chatbot.main import app
from chatbot.core.database import Base, engine
from sqlalchemy.orm import sessionmaker
import os

# Test-Datenbank einrichten
TestingSessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
Base.metadata.create_all(bind=engine)

client = TestClient(app)

# Testdaten
TEST_USER = {
    "username": "testuser",
    "email": "testuser@example.com",
    "password": os.environ.get("TEST_USER_PASSWORD", "defaultpassword")
}

@pytest.fixture(scope="module", autouse=True)
def setup_database():
    """Stellt sicher, dass die Datenbank vor den Tests sauber ist."""
    Base.metadata.drop_all(bind=engine)  # Tabellen löschen
    Base.metadata.create_all(bind=engine)  # Tabellen neu erstellen
    yield
    Base.metadata.drop_all(bind=engine)  # Aufräumen nach den Tests

def test_register_user():
    response = client.post("/api/register", json=TEST_USER)
    assert response.status_code == 201, response.text
    data = response.json()
    assert data["username"] == TEST_USER["username"]
    assert data["email"] == TEST_USER["email"]
    assert "id" in data
    assert data["id"] is not None, "ID sollte nicht None sein"  # Debugging-Check

def test_login_user():
    # Benutzer registrieren
    client.post("/api/register", json=TEST_USER)

    # Login testen
    response = client.post("/api/login", data={
        "username": TEST_USER["username"],
        "password": TEST_USER["password"]
    })
    assert response.status_code == 200, response.text
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"