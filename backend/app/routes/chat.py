from fastapi import APIRouter

from backend.app.schemas.chat import ChatRequest
from backend.app.services.rag_service import answer_question


router = APIRouter()


@router.post("/chat")
def chat(request: ChatRequest):
    answer = answer_question(request.question)

    return {
        "question": request.question,
        "answer": answer
    }