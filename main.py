from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from rag import ask_nexora




app = FastAPI(
    title="Nexora Support Assistant",
    description="RAG-based customer support API",
    version="1.0.0"
)



app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



class ChatRequest(BaseModel):
    question: str



class ChatResponse(BaseModel):
    answer: str
    sources: list[str]




@app.get("/")
def root():
    return {
        "message": "Nexora Support Assistant API is running"
    }



@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):

    question = request.question.strip()

    if not question:
        return {
            "answer": "Please enter a question.",
            "sources": []
        }

    result = ask_nexora(question)

    return {
        "answer": result["answer"],
        "sources": result["sources"]
    }