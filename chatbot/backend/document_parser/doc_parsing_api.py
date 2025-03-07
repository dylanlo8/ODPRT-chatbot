from fastapi import FastAPI, HTTPException, APIRouter, UploadFile, File
from pydantic import BaseModel
from typing import List
import os
import pickle
import shutil
from chatbot.backend.document_parser.document_parser import DocumentParser

# ==========================
# Initialize FastAPI and DocumentParser
# ==========================
app = FastAPI()
document_parser = DocumentParser()

document_parser_router = APIRouter(prefix="/document-parser")

# ==========================
# Pydantic Models
# ==========================

class ProcessUserUploads(BaseModel):
    text_chunks: List[str]
    # image_summaries: List[str]

# ==========================
# API Endpoints
# ==========================

@document_parser_router.post("/process-upload/", response_model=ProcessUserUploads)
async def process_upload(file: UploadFile = File(...)):
    """
    API endpoint to process a user-uploaded document:
    1. Saves the uploaded file.
    2. Calls `process_user_uploads` from `DocumentParser`.
    3. Returns the list of text chunks and image summaries.
    
    Args:
        file (UploadFile): The uploaded file.
    
    Returns:
        dict: A dictionary containing a list of text chunks and a list of image summaries.
    """
    upload_dir = "uploads"
    os.makedirs(upload_dir, exist_ok=True)
    file_path = os.path.join(upload_dir, file.filename)
    
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    text_chunks = document_parser.process_user_uploads(file_path)
    
    os.remove(file_path)

    return {"text_chunks": text_chunks}
