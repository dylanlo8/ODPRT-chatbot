"""
This module defines the API endpoints for handling chat queries and email escalations.
It uses FastAPI for routing and Pydantic for request validation.
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel  # Import Pydantic's BaseModel
from chatbot.backend.inference.response_generator import ResponseGenerator
from chatbot.backend.services.vector_db.db import vector_db
import requests
import httpx

# URL for hybrid search in the vector database
HYBRID_SEARCH_URL = "http://localhost:8000/vector-db/hybrid-search/"
# Instance of the ResponseGenerator class for generating responses and emails
response_generator = ResponseGenerator()

# ==========================
# FastAPI Router for Chat Queries
# ==========================
# FastAPI router for chat-related endpoints
chat_router = APIRouter(prefix="/chat")


# Define a Pydantic model for the request body
class ChatQueryRequest(BaseModel):  # Pydantic model for chat query requests
    """
    Represents the request body for a chat query.

    Attributes:
        user_query (str): The user's query.
        uploaded_content (str): Optional content uploaded by the user.
        chat_history (str): Optional chat history.
    """
    user_query: str
    uploaded_content: str = ""
    chat_history: str = ""

class EmailEscalationRequest(BaseModel):  # Pydantic model for email escalation requests
    """
    Represents the request body for an email escalation.

    Attributes:
        chat_history (str): The chat history to be included in the email.
    """
    chat_history: str = ""

@chat_router.post("/query/")  # Endpoint for handling chat queries
async def chat_query(request: ChatQueryRequest) -> dict:  # Use the Pydantic model
    """
    Handles a chat query by processing the user's input and returning a response.

    Args:
        request (ChatQueryRequest): The request body containing user query, uploaded content, and chat history.

    Returns:
        dict: A dictionary containing the generated answer.
    """
    try:  # Attempt to process the query
        answer = response_generator.query_workflow(
            user_query=request.user_query,
            uploaded_content=request.uploaded_content,
            chat_history=request.chat_history,
        )

        return {"answer": answer}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))  # Handle errors gracefully
    
@chat_router.post("/email-escalation/")  # Endpoint for handling email escalations
async def email_escalation(request: EmailEscalationRequest) -> dict:  # Use the Pydantic model
    """
    Handles email escalation by generating an email based on the chat history.

    Args:
        request (EmailEscalationRequest): The request body containing chat history.

    Returns:
        dict: A dictionary containing the email subject, body, and recipients.
    """
    try:  # Attempt to generate the email
        # Get the email subject, body, and recipients
        email_subject, email_body, _ = response_generator.generate_email(
            chat_history=request.chat_history
        )
        
        # Redirect all email escalations to a predefined recipient
        temp_recipient = ["iep-admin@nus.edu.sg"]

        return {"email_subject": email_subject, "email_body": email_body, "email_recipients": temp_recipient}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
