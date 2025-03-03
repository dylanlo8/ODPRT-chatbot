from fastapi import APIRouter, HTTPException
from pydantic import BaseModel  # Import Pydantic's BaseModel
from chatbot.backend.inference.response_generator import ResponseGenerator
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
        
        async with httpx.AsyncClient() as client:  # Use httpx for async requests
            hybrid_search_response = await client.post(HYBRID_SEARCH_URL, json=search_query, timeout=10)
        context = hybrid_search_response.json()["context"]
        
        # TODO: Retrieve chat history and uploaded Content
        
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