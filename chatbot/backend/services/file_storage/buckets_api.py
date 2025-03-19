from fastapi import FastAPI, HTTPException, UploadFile, File, APIRouter
from pydantic import BaseModel
from chatbot.backend.services.file_storage.buckets import upload_file, delete_file, fetch_files
import os

# ==========================
# Pydantic Models
# ==========================

class DeleteFileRequest(BaseModel):
    file_names: list[str]

# ==========================
# FastAPI Router
# ==========================
buckets_router = APIRouter(prefix="/buckets")

@buckets_router.post("/upload/")
async def upload_file_endpoint(files: list[UploadFile] = File(...)):
    try:
        responses = []
        for file in files:
            # Save the uploaded file temporarily
            temp_file_path = f"temp_{file.filename}"
            with open(temp_file_path, "wb") as buffer:
                buffer.write(await file.read())
            
            # Call the upload function
            response = upload_file(temp_file_path, file.filename)
            responses.append(response)
            
            # Remove the temporary file after upload
            os.remove(temp_file_path)
        
        return responses
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@buckets_router.get("/fetch-files")
async def fetch_files_endpoints():
    try:
        response = fetch_files()
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

@buckets_router.get("/fetch-files")
async def fetch_file_endpoint(
    folder: str = "", 
    limit: int = 100, 
    offset: int = 0, 
    sort_by_column: str = "name", 
    sort_by_order: str = "desc"
    ):

    try:
        sort_by = {"column": sort_by_column, "order": sort_by_order}
        response = fetch_files(folder, limit, offset, sort_by)
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))