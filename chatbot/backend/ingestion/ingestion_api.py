from fastapi import APIRouter, HTTPException, UploadFile, File
from pydantic import BaseModel
from chatbot.backend.ingestion.ingestion_service import IngestionService
from chatbot.backend.document_parser.document_parser import DocumentParser
import shutil
import os

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
        # Preprocessing and storing in Buckets stage
        # Images
        if file.content_type.startswith('image/'):
            try:
                # Save the uploaded image file to a temporary location
                temp_file_path = f"/tmp/{file.filename}"
                with open(temp_file_path, "wb") as buffer:
                    shutil.copyfileobj(file.file, buffer)
                
                # Ingest the image
                ingestion_service.ingest_images([temp_file_path])

                # Remove temp_file traces at end of ingestion
                temp_file_paths.append(temp_file_path)
            except Exception as e:
                raise HTTPException(status_code=500, detail=f"Failed to save or ingest image file {file.filename}: {str(e)}")
            
        # PDF or DOCX Files
        elif file.content_type in ['application/pdf', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document']:
            doc_source = file.filename
            doc_type = "Word Documents / PDF"
            
            try:
                # Save the uploaded document file to a temporary location
                temp_file_path = f"/tmp/{file.filename}"
                with open(temp_file_path, "wb") as buffer:
                    shutil.copyfileobj(file.file, buffer)

                # Extract text from the document
                extracted_text = document_parser.process_user_uploads(temp_file_path)

                # Ingest the text documents
                ingestion_service.ingest_texts(extracted_text, doc_source, doc_type)

                # Remove temp_file traces at end of ingestion
                temp_file_paths.append(temp_file_path)
            except Exception as e:
                raise HTTPException(status_code=500, detail=f"Failed to save or ingest document file {file.filename}: {str(e)}")
        else:
            raise HTTPException(status_code=400, detail=f"Invalid file type for {file.filename}. Only image, PDF, and DOCX files are allowed.")
    
    # Remove temporary files
    for temp_file_path in temp_file_paths:
        try:
            os.remove(temp_file_path)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to remove temporary file {temp_file_path}: {str(e)}")
    
    return {"message": "Files ingested successfully"}