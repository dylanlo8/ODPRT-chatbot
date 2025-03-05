from fastapi import APIRouter, HTTPException, UploadFile, File
from pydantic import BaseModel
from chatbot.backend.ingestion.ingestion_service import IngestionService
from chatbot.backend.document_parser.document_parser import DocumentParser
import shutil

ingestion_router = APIRouter(prefix="/ingestion")
ingestion_service = IngestionService()
document_parser = DocumentParser()

class TextIngestionRequest(BaseModel):
    text_chunks: list
    doc_source: str
    doc_type: str

@ingestion_router.post("/ingest-images/")
async def ingest_images(files: list[UploadFile] = File(...)):
    image_paths = []

    for file in files:
        # Check if its an image
        if file.content_type.startswith('image/'):
            try:
                # Save the uploaded file to a temporary location
                temp_file_path = f"/tmp/{file.filename}"
                with open(temp_file_path, "wb") as buffer:
                    shutil.copyfileobj(file.file, buffer)

                # Append the file path to the list of image paths
                image_paths.append(temp_file_path)
            except Exception as e:
                raise HTTPException(status_code=500, detail=f"Failed to save file {file.filename}: {str(e)}")
        else:
            raise HTTPException(status_code=400, detail=f"Invalid file type for {file.filename}. Only image files are allowed.")
    
    # Sends the temporarily saved image paths to the ingestion service
    try:
        # Ingest the images
        ingestion_service.ingest_images(image_paths)
        return {"message": "Images ingested successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@ingestion_router.post("/ingest-texts/")
async def ingest_texts(request: TextIngestionRequest):
    try:
        ingestion_service.ingest_texts(request.text_chunks, request.doc_source, request.doc_type)
        return {"message": "Texts ingested successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@ingestion_router.post("/ingest-files/")
async def ingest_files(files: list[UploadFile] = File(...)):
    image_paths = []
    text_chunks = []
    doc_source = "uploaded_files"
    doc_type = "Documents"

    for file in files:
        if file.content_type.startswith('image/'):
            try:
                # Save the uploaded image file to a temporary location
                temp_file_path = f"/tmp/{file.filename}"
                with open(temp_file_path, "wb") as buffer:
                    shutil.copyfileobj(file.file, buffer)
                image_paths.append(temp_file_path)
            except Exception as e:
                raise HTTPException(status_code=500, detail=f"Failed to save image file {file.filename}: {str(e)}")
            
        # PDF or DOCX Files
        elif file.content_type in ['application/pdf', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document']:
            try:
                # Save the uploaded document file to a temporary location
                temp_file_path = f"/tmp/{file.filename}"
                with open(temp_file_path, "wb") as buffer:
                    shutil.copyfileobj(file.file, buffer)
                # Extract text from the document
                extracted_text = document_parser.process_user_uploads(temp_file_path)
                text_chunks.extend(extracted_text)
            except Exception as e:
                raise HTTPException(status_code=500, detail=f"Failed to save document file {file.filename}: {str(e)}")
        else:
            raise HTTPException(status_code=400, detail=f"Invalid file type for {file.filename}. Only image, PDF, and DOCX files are allowed.")
    
    # Ingest the images
    if image_paths:
        try:
            ingestion_service.ingest_images(image_paths)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to ingest images: {str(e)}")
    
    # Ingest the text documents
    if text_chunks:
        try:
            ingestion_service.ingest_texts(text_chunks, doc_source, doc_type)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to ingest text documents: {str(e)}")
    
    return {"message": "Files ingested successfully"}