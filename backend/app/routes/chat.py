from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()


class ChatRequest(BaseModel):
    question: str


@router.post("/chat")
def chat(request: ChatRequest):
    return {
        "question": request.question,
        "answer": "KnowledgeOS will answer this using your documents."
    }