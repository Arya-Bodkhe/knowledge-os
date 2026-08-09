from fastapi import FastAPI
from backend.app.routes.chat import router as chat_router
from backend.app.routes.documents import router as documents_router

app = FastAPI()

app.include_router(chat_router)
app.include_router(documents_router)

@app.get("/")
def home():
    return {"message": "Welcome to KnowledgeOS!"}


@app.get("/health")
def health_check():
    return {"status": "healthy"}