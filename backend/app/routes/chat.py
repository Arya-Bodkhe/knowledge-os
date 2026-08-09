from fastapi import APIRouter
from backend.app.schemas.chat import ChatRequest

router = APIRouter()

@router.post("/chat")
def chat(request: ChatRequest):
    return {
        "question": request.question,
        "answer": "KnowledgeOS will answer this using your documents."
    }