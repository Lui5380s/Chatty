from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class ChatRequest(BaseModel):
    project: Optional[str] = Field(
        None,
        description="Testweise Projektname (für Kontext / Personalisierung)."
    )
    user: Optional[str] = Field(
        None,
        description="Benutzername (für Berechtigungen / Logging)."
    )
    message: str = Field(..., min_length=1, description="Die Nutzernachricht an den Chatbot.")

class ChatResponse(BaseModel):
    user_input: str = Field(..., description="Die originale Nutzernachricht")
    chatty_response: str = Field(..., description="Die vom Chatbot erzeugte Antwort")
    project: Optional[str] = Field(None, description="Das verwendete Projekt (falls angegeben)")
    source: Optional[str] = Field(None, description="Optional: Quelle / Hinweis wie die Antwort gefunden wurde")

class ProjectBase(BaseModel):
    name: str
    description: Optional[str] = None


class ProjectCreate(ProjectBase):
    """Wird für POST /api/projects benutzt."""
    pass


class ProjectRead(ProjectBase):
    """Wird für GET /api/projects oder GET /api/projects/{id} benutzt."""
    id: int
    created_at: datetime

    class ConfigDict:
        from_attributes = True  # erlaubt ORM -> Schema Konvertierung

class UserBase(BaseModel):
    username: str
    email: str
    is_active: bool = True
    is_superuser: bool = False

class UserCreate(UserBase):
    password: str

class UserRead(UserBase):
    id: int

    class Config:
        from_attributes = True