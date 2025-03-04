from fastapi import FastAPI, HTTPException, APIRouter
from pydantic import BaseModel
from typing import List
import os
import pickle
from chatbot.backend.services.document_parser import DocumentParser

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
