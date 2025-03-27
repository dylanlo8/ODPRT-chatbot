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

class EmailEscalationRequest(BaseModel):
    chat_history: str = ""

@chat_router.post("/query/")
async def chat_query(request: ChatQueryRequest) -> dict:  # Use the Pydantic model
    try:
        answer = response_generator.query_workflow(
            user_query=request.user_query,
            uploaded_content=request.uploaded_content,
            chat_history=request.chat_history,
        )

        return {"answer": answer}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@chat_router.post("/email-escalation/")
async def email_escalation(request: EmailEscalationRequest) -> dict:  # Use the Pydantic model
    try:
        # Get the email subject, body, and recipients
        email_subject, email_body, _ = response_generator.generate_email(
            chat_history=request.chat_history
        )
        
        # Re-direct all email escalations to iep-admin@nus.edu.sg
        temp_recipient = ["iep-admin@nus.edu.sg"]

        return {"email_subject": email_subject, "email_body": email_body, "email_recipients": temp_recipient}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
