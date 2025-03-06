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
class ProcessAttachmentsResponse(BaseModel):
    message: str
    processed_files: List[str]

class ExtractResponse(BaseModel):
    text: str
    images: List[str]

class ChunkTextResponse(BaseModel):
    chunks: List[str]

class ProcessUserUploads(BaseModel):
    text_chunks: List[str]
    # image_summaries: List[str]

# ==========================
# API Endpoints
# ==========================

@document_parser_router.post("/process-attachments/", response_model=ProcessAttachmentsResponse)
async def process_attachments():
    try:
        processed_files = document_parser.process_and_save_attachments()
        return {"message": "Attachments processed successfully", "processed_files": processed_files}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@document_parser_router.post("/extract-text-and-images/", response_model=ExtractResponse)
async def extract_text_and_images(file_path: str):
    try:
        text, images, _ = document_parser.separate_text_and_images(file_path)
        return {"text": text, "images": images}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@document_parser_router.post("/chunk-text/", response_model=ChunkTextResponse)
async def chunk_text(text: str):
    try:
        chunks = document_parser.chunk_text(text)
        return {"chunks": chunks}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    


@document_parser_router.get("/get-processed-data/")
async def get_processed_data():
    try:
        root_pkl_dir = os.path.join(os.getcwd(), "data_pkl")
        if not os.path.exists(root_pkl_dir):
            return {"message": "No processed data found."}

        processed_data = {}
        for folder in os.listdir(root_pkl_dir):
            folder_path = os.path.join(root_pkl_dir, folder)
            if os.path.isdir(folder_path):
                text_pickle = os.path.join(folder_path, "text_chunks.pkl")
                images_pickle = os.path.join(folder_path, "images.pkl")
                
                if os.path.exists(text_pickle):
                    with open(text_pickle, "rb") as f:
                        processed_data[folder] = {"text_chunks": pickle.load(f)}
                if os.path.exists(images_pickle):
                    with open(images_pickle, "rb") as f:
                        processed_data[folder]["images"] = pickle.load(f)
        
        return processed_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
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
