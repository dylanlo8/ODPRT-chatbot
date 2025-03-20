import os
import io
import mimetypes
from fastapi import FastAPI, HTTPException, UploadFile, File, APIRouter, Query
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from chatbot.backend.services.file_storage.buckets import upload_file, delete_file, fetch_files, download_file

# ==========================
# Pydantic Models
# ==========================

class DeleteFileRequest(BaseModel):
    file_names: list[str]

class FetchFilesRequest(BaseModel):
    folder: str = ""
    limit: int = 100
    offset: int = 0
    sort_by_column: str = "name"
    sort_by_order: str = "desc"

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
async def fetch_file_endpoint(request: FetchFilesRequest):
    try:
        sort_by = {"column": request.sort_by_column, "order": request.sort_by_order}
        response = fetch_files(request.folder, request.limit, request.offset, sort_by)
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@buckets_router.get("/download-file")
async def download_file_endpoint(file_path: str = Query(...)):
    try: 
        response = download_file(file_path)

        # Create an in-memory file object
        file_stream = io.BytesIO(response)

        # Determine MIME type
        mime_type, _ = mimetypes.guess_type(file_path)
        mime_type = mime_type or "application/octet-stream"

        headers = {
            "Content-Disposition": f'attachment; filename="{file_path.split("/")[-1]}"'
        }

        return StreamingResponse(file_stream, media_type=mime_type, headers=headers)
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))