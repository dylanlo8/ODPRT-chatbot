from fastapi import FastAPI, HTTPException, APIRouter
from pydantic import BaseModel
from typing import List
from chatbot.backend.faq_parser.faq_parser import FAQ_Parser

# ==========================
# Initialize FastAPI and FAQ_Parser
# ==========================
app = FastAPI()
faq_parser = FAQ_Parser()

faq_parser_router = APIRouter(prefix="/faq-parser")

# ==========================
# Pydantic Models
# ==========================
class QAPairsResponse(BaseModel):
    qa_pairs: List[str]

class ExtractedTextResponse(BaseModel):
    text: str

# ==========================
# API Endpoints
# ==========================

@faq_parser_router.post("/extract-faq-text/", response_model=ExtractedTextResponse)
async def extract_faq_text():
    try:
        text = faq_parser.extract_faq()
        return {"text": text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@faq_parser_router.post("/get-qa-pairs/", response_model=QAPairsResponse)
async def get_qa_pairs():
    try:
        qa_pairs = faq_parser.get_qa_pairs()
        return {"qa_pairs": qa_pairs}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))