from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class ChatRequest(BaseModel):
    question: str

@app.get("/")
def home():
    return {"message": "Welcome to KnowledgeOS!"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}

@app.post("/chat")
def chat(request: ChatRequest):
    return {
        "question": request.question,
        "answer": "KnowledgeOS will answer this using your documents."
    }