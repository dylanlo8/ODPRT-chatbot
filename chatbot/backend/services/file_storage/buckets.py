import os
import mimetypes
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()
url: str = os.environ.get("SUPABASE_URL")
service_key: str = os.environ.get("SUPABASE_SERVICE_KEY") # Requires service role key to bypass RLS
supabase: Client = create_client(url, supabase_key=service_key)

BUCKET_NAME = "rag_files"

# Some examples of MIME File Types
# text/plain, image/png, image/jpeg, image/jpg, application/pdf

def upload_file(source_file_path: str, destination_file_path: str) -> dict:
    """
    Uploads a file to the bucket
    """
    try:
        # Identify the content type
        content_type, _ = mimetypes.guess_type(source_file_path)
        if content_type is None:
            # .msg files cannot be guessed, check if path is a .msg file
            if source_file_path.endswith(".msg"):
                content_type = 'application/vnd.ms-outlook'
            else:
                content_type = 'application/octet-stream'  # Default content type

        # Open the file in binary mode for uploading
        with open(source_file_path, 'rb') as file:
            response = supabase.storage.from_(BUCKET_NAME).upload(
                destination_file_path, 
                file,
                {"content-type": content_type}
            )
        return response
    except Exception as exception:
        return exception
    
def delete_file(file_names: list[str]) -> dict:
    """
    Bulk deletes files from the bucket
    """
    try:
        response = supabase.storage.from_(BUCKET_NAME).remove(file_names)
        return response
    except Exception as exception:
        return exception
    
# SAMPLE EXECUTION
# response = upload_file("email.msg", "email.msg")
# print(response)

# response = delete_file(["email.msg"])
# print(response)