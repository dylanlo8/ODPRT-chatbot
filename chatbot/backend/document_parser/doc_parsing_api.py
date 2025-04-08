"""
This module defines the API endpoints for processing user-uploaded documents.
It uses FastAPI for routing and integrates with the DocumentParser class to handle document parsing.
"""

from fastapi import FastAPI, HTTPException, APIRouter, UploadFile, File
from pydantic import BaseModel
from typing import List
import os
import pickle
import shutil
from chatbot.backend.document_parser.document_parser import DocumentParser

# Initialize FastAPI application and DocumentParser instance
app = FastAPI()
document_parser = DocumentParser()

document_parser_router = APIRouter(prefix="/document-parser")

# Define Pydantic models for request and response validation
class ProcessUserUploads(BaseModel):
    text_chunks: List[str]
    # image_summaries: List[str]

# Define API endpoints for document processing
@document_parser_router.post("/process-upload/", response_model=ProcessUserUploads)
async def process_upload(file: UploadFile = File(...)):
    """
    Processes a user-uploaded document by saving it, parsing its content, and returning the results.

    Steps:
    1. Save the uploaded file.
    2. Parse the file using `DocumentParser`.
    3. Return the parsed text chunks.

    Args:
        file (UploadFile): The uploaded file.
    
    Returns:
        dict: A dictionary containing a list of text chunks.
    """
    upload_dir = "uploads"
    os.makedirs(upload_dir, exist_ok=True)
    file_path = os.path.join(upload_dir, file.filename)
    
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    text_chunks = document_parser.process_user_uploads(file_path)
    
    os.remove(file_path)

    return {"text_chunks": text_chunks}
