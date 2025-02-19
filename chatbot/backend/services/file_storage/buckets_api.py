from fastapi import FastAPI, HTTPException, UploadFile, File, APIRouter
from pydantic import BaseModel
from chatbot.backend.services.file_storage.buckets import upload_file, delete_file
import os

# ==========================
# Pydantic Models
# ==========================

class DeleteFileRequest(BaseModel):
    file_names: list[str]

# ==========================
# FastAPI Router
# ==========================
buckets_router = APIRouter(prefix="/buckets-api")

@buckets_router.post("/upload")
async def upload_file_endpoint(file: UploadFile = File(...)):
    try:
        # Save the uploaded file temporarily
        temp_file_path = f"temp_{file.filename}"
        with open(temp_file_path, "wb") as buffer:
            buffer.write(await file.read())
        
        # Call the upload function
        response = upload_file(temp_file_path, file.filename)
        
        # Remove the temporary file after upload
        os.remove(temp_file_path)
        
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@buckets_router.delete("/delete")
async def delete_file_endpoint(request: DeleteFileRequest):
    try:
        response = delete_file(request.file_names)
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))