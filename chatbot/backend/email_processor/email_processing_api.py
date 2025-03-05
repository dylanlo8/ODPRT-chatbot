from fastapi import FastAPI, HTTPException, APIRouter
from pydantic import BaseModel
from typing import List
from chatbot.backend.services.email_processor.email_processor import EmailProcessor

# ==========================
# Initialize FastAPI and EmailProcessor
# ==========================
app = FastAPI()
email_processor = EmailProcessor()

email_processor_router = APIRouter(prefix="/email-processor")

# ==========================
# Pydantic Models
# ==========================
class QAPairsResponse(BaseModel):
    qa_pairs: List[str]

class UsefulEmailsResponse(BaseModel):
    useful_emails: List[str]

# ==========================
# API Endpoints
# ==========================

@email_processor_router.post("/filter-useful-emails/", response_model=UsefulEmailsResponse)
async def filter_useful_emails():
    try:
        useful_emails = email_processor._filter_useful_emails()
        return {"useful_emails": useful_emails}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@email_processor_router.post("/get-qa-pairs/", response_model=QAPairsResponse)
async def get_qa_pairs():
    try:
        qa_pairs = email_processor.get_qa_pairs()
        return {"qa_pairs": qa_pairs}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
