from fastapi.testclient import TestClient
from chatbot.main import app

client = TestClient(app)

def test_chat_valid_message():
    payload = {
        "project": "test_project",
        "user": "luis",
        "message": "Hallo Chatty!"
    }
    resp = client.post("/api/chat", json=payload)
    assert resp.status_code == 200
    data = resp.json()
    assert data["user_input"] == payload["message"]
    assert "chatty_response" in data
    assert data["project"] == payload["project"]

def test_chat_empty_message():
    payload = {"message": ""}
    resp = client.post("/api/chat", json=payload)
    assert resp.status_code == 422