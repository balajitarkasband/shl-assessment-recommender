from fastapi import APIRouter
from app.models import ChatRequest
from app.chat_logic import handle_chat

router = APIRouter()


@router.get("/health")
def health():
    return {"status": "ok"}


@router.post("/chat")
def chat(request: ChatRequest):
    response = handle_chat(request.messages)
    return response