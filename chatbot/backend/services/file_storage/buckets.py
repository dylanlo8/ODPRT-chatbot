import os
import io
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
    Uploads a file to the bucket.

    Args:
        source_file_path (str): The local path of the file to be uploaded.
        destination_file_path (str): The path where the file will be stored in the bucket.

    Returns:
        dict: Response from the storage service or an exception in case of failure.
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
    
def fetch_files(
        folder: str = "", 
        limit: int = 100, 
        offset: int = 0, 
        sort_by: dict = {"column": "name", "order": "desc"}
    ) -> dict:

    """
    Fetches a list of files from the specified folder in the bucket.

    Args:
        folder (str): The folder path in the bucket to fetch files from. Defaults to "".
        limit (int): The maximum number of files to fetch. Defaults to 100.
        offset (int): The starting point for fetching files. Defaults to 0.
        sort_by (dict): Sorting criteria with keys 'column' and 'order'. Defaults to {"column": "name", "order": "desc"}.

    Returns:
        dict: Response containing the list of files or an exception in case of failure.
    """
    try:
        response = supabase.storage.from_(BUCKET_NAME).list(  # Await here
            folder,
            {
                "limit": limit,
                "offset": offset,
                "sortBy": sort_by,
            }
        )
        return response
    except Exception as exception:
        return exception

    
def delete_file(file_names: list[str]) -> dict:
    """
    Bulk deletes files from the bucket.

    Args:
        file_names (list[str]): List of file names to be deleted.

    Returns:
        dict: Response from the storage service or an exception in case of failure.
    """
    try:
        response = supabase.storage.from_(BUCKET_NAME).remove(file_names)
        return response
    except Exception as exception:
        return exception
    
def download_file(file_path):
    """
    Downloads a file from the bucket.

    Args:
        file_path (str): The path of the file to be downloaded.

    Returns:
        Any: The downloaded file content or an exception in case of failure.
    """
    try: 
        response = supabase.storage.from_(BUCKET_NAME).download(file_path)
        return response
    except Exception as exception:
        return exception
