import os
import pickle
import requests
from chatbot.backend.services.models.embedding_model import embedding_model  # Ensure this import is present

def ingest_text_documents():
    # Define the directory containing the pickle files
    pkl_dir = "chatbot/backend/data_pkl"
    
    # Iterate through all subdirectories in the pkl_dir
    for dir in os.listdir(pkl_dir):
        sub_dir_path = os.path.join(pkl_dir, dir)
        if os.path.isdir(sub_dir_path):  # Check if it's a directory
            # Walk through each subdirectory to find .pkl files
            for root, _, files in os.walk(sub_dir_path):
                for filename in files:
                    file_path = os.path.join(root, filename)

                    if filename.endswith(".pkl"):
                        # Load the text chunks from the pickle file
                        with open(file_path, "rb") as f:
                            text_chunks = pickle.load(f)

                        # Embed the text Chunks
                        dense_embeddings, sparse_embeddings = embedding_model.encode_texts(text_chunks)

                        # Prepare the payload for ingestion
                        doc_type = "FAQ" if "faq" in filename.lower() else "Emails"  # Determine doc_source based on filename
                        payload = {
                            "data": [
                                [doc_type] * len(text_chunks), # doc_name
                                [dir] * len(text_chunks),  # Use the subdirectory name as doc_source
                                text_chunks, # text
                                dense_embeddings,  # Dense embeddings
                                embedding_model.convert_sparse_embeddings(sparse_embeddings),  # payload sparse embeddings
                            ]
                        }

                        # Ingest the original email attachment into the vector database via API
                        try:
                            response = requests.post("http://localhost:8000/vector-db/insert-documents/", json=payload)
                            response.raise_for_status()  # Raise an error for bad responses
                            print(f"Successfully ingested data from {filename}: {response.json()}")
                        except Exception as e:
                            print(f"Failed to ingest data from {filename}: {str(e)}")

                    # Upload the mail original documents into the FileStorage
                    if filename.endswith(".msg"):
                        try:
                            with open(file_path, "rb") as f:
                                files = {'file': (filename, f)}
                                upload_response = requests.post("http://localhost:8000/buckets-api/upload", files=files)
                                upload_response.raise_for_status()  # Raise an error for bad responses
                                print(f"Uploaded {filename} to file storage: {upload_response.json()}")
                        except Exception as e:
                            print(f"Failed to upload {filename} to file storage: {str(e)}")

if __name__ == "__main__":
    ingest_text_documents()


