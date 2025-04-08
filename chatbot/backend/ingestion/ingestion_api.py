import logging
from fastapi import APIRouter, HTTPException, UploadFile, File
from pydantic import BaseModel
from chatbot.backend.ingestion.ingestion_service import IngestionService
from chatbot.backend.document_parser.document_parser import DocumentParser
import shutil
import os

"""
This module defines the ingestion API for handling file uploads and processing.
It includes endpoints for ingesting various file types such as images, PDFs, and Word documents.
"""
# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

ingestion_router = APIRouter(prefix="/ingestion")
ingestion_service = IngestionService()
document_parser = DocumentParser()

class TextIngestionRequest(BaseModel):
    text_chunks: list
    doc_source: str
    doc_type: str
    
@ingestion_router.post("/ingest-files/")
async def ingest_files(files: list[UploadFile] = File(...)):
    temp_file_paths = []

    for file in files:
        logger.info(f"Processing file: {file.filename} with content type: {file.content_type}")
        try:
            # Images
            if file.content_type.startswith('image/'):
                temp_file_path = f"/tmp/{file.filename}"
                with open(temp_file_path, "wb") as buffer:
                    shutil.copyfileobj(file.file, buffer)
                logger.info(f"Saved image file to {temp_file_path}")
                ingestion_service.ingest_images([temp_file_path])
                temp_file_paths.append(temp_file_path)
            
            # PDF or DOCX Files
            elif file.content_type in ['application/pdf', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document']:
                temp_file_path = f"/tmp/{file.filename}"
                with open(temp_file_path, "wb") as buffer:
                    shutil.copyfileobj(file.file, buffer)
                logger.info(f"Saved document file to {temp_file_path}")
                extracted_text = document_parser.process_user_uploads(temp_file_path)
                ingestion_service.ingest_texts(extracted_text, file.filename, "Word Documents / PDF")
                temp_file_paths.append(temp_file_path)
            
            else:
                raise HTTPException(status_code=400, detail=f"Invalid file type for {file.filename}.")
        
        except Exception as e:
            logger.error(f"Error processing file {file.filename}: {str(e)}", exc_info=True)
            raise HTTPException(status_code=500, detail=f"Failed to process file {file.filename}: {str(e)}")
    
    for temp_file_path in temp_file_paths:
        try:
            os.remove(temp_file_path)
            logger.info(f"Removed temporary file {temp_file_path}")
        except Exception as e:
            logger.error(f"Failed to remove temporary file {temp_file_path}: {str(e)}", exc_info=True)
            raise HTTPException(status_code=500, detail=f"Failed to remove temporary file {temp_file_path}: {str(e)}")
    
    return {"message": "Files ingested successfully"}
