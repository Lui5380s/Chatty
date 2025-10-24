from fastapi import APIRouter, HTTPException
from chatbot.api.schemas import ChatRequest, ChatResponse
from chatbot.core.model_manager import generate_response
from typing import Any

router = APIRouter(tags=["Chat"])

@router.post("/chat", response_model=ChatResponse)
async def chat_endpoint(payload: ChatRequest) -> Any:
    """
    POST /api/chat
    Body: { "project": "...", "user": "...", "message": "..." }
    """
    # einfache validation / placeholders (später: permission check, project exists etc.)
    if not payload.message or payload.message.strip() == "":
        raise HTTPException(status_code=400, detail="Message must not be empty")

    # hier rufst du später model_manager/retriever mit payload.project etc. auf
    reply = generate_response(payload.message)

    return ChatResponse(
        user_input=payload.message,
        chatty_response=reply,
        project=payload.project,
        source="local-rule-based"  # später: e.g. "db", "llm", "faq"
    )