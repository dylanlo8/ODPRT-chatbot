from fastapi import APIRouter, HTTPException
from pydantic import BaseModel  # Import Pydantic's BaseModel
from chatbot.backend.inference.response_generator import ResponseGenerator

# ==========================
# FastAPI Router for Chat Queries
# ==========================
chat_router = APIRouter(prefix="/chat")

response_generator = ResponseGenerator()

# Define a Pydantic model for the request body
class ChatQueryRequest(BaseModel):
    user_query: str
    uploaded_content: str = ""
    context: str = ""
    chat_history: str = ""

@chat_router.post("/query/")
async def chat_query(request: ChatQueryRequest) -> dict:  # Use the Pydantic model
    try:
        answer = response_generator.query_workflow(
            user_query=request.user_query,
            uploaded_content=request.uploaded_content,
            context=request.context,
            chat_history=request.chat_history,
        )
        return {"answer": answer}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))