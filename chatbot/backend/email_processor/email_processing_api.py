"""
This module defines the API endpoints for processing emails.
It uses FastAPI for routing and integrates with the EmailProcessor class to handle email filtering and QA pair extraction.
"""

from fastapi import FastAPI, HTTPException, APIRouter
from pydantic import BaseModel
from typing import List
from chatbot.backend.email_processor.email_processor import EmailProcessor

# Initialize FastAPI application and EmailProcessor instance
app = FastAPI()
email_processor = EmailProcessor()

email_processor_router = APIRouter(prefix="/email-processor")

# Define Pydantic models for request and response validation
class QAPairsResponse(BaseModel):
    qa_pairs: List[str]

class UsefulEmailsResponse(BaseModel):
    useful_emails: List[str]

# Define API endpoints for email processing
@email_processor_router.post("/filter-useful-emails/", response_model=UsefulEmailsResponse)
async def filter_useful_emails():
    """
    Filters useful emails by processing the email data and identifying relevant content.

    Returns:
        dict: A dictionary containing a list of useful emails.
    """
    try:  # Attempt to filter useful emails
        useful_emails = email_processor._filter_useful_emails()
        return {"useful_emails": useful_emails}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@email_processor_router.post("/get-qa-pairs/", response_model=QAPairsResponse)
async def get_qa_pairs():
    """
    Extracts question-answer pairs from emails.

    Returns:
        dict: A dictionary containing a list of QA pairs.
    """
    try:  # Attempt to extract QA pairs
        qa_pairs = email_processor.get_qa_pairs()
        return {"qa_pairs": qa_pairs}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
