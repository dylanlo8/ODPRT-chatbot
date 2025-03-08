from fastapi import APIRouter, HTTPException
from pydantic import BaseModel  # Import Pydantic's BaseModel
from chatbot.backend.inference.response_generator import ResponseGenerator
from chatbot.backend.services.vector_db.db import vector_db
import requests
import httpx

HYBRID_SEARCH_URL = "http://localhost:8000/vector-db/hybrid-search/"
response_generator = ResponseGenerator()

# ==========================
# FastAPI Router for Chat Queries
# ==========================
chat_router = APIRouter(prefix="/chat")

# Define a Pydantic model for the request body
class ChatQueryRequest(BaseModel):
    user_query: str
    uploaded_content: str = ""
    chat_history: str = ""

@chat_router.post("/query/")
async def chat_query(request: ChatQueryRequest) -> dict:  # Use the Pydantic model
    try:
        # Perform Hybrid Search RAG to retrieve context based on query
        search_query = {
            "query": request.user_query 
        }
        
        context = vector_db.hybrid_search(search_query['query'])
        
        # Prepare Query Workflow
        answer = response_generator.query_workflow(
            user_query=request.user_query,
            uploaded_content=request.uploaded_content,
            context=context,
            chat_history=request.chat_history,
        )

        return {"answer": answer}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))