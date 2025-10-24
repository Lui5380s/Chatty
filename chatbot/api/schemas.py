from pydantic import BaseModel, Field
from typing import Optional

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