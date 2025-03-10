import os
import pickle
import requests
from chatbot.backend.services.models.embedding_model import embedding_model
from chatbot.backend.services.vector_db.db import vector_db

# Ensure that API Service is up and running
# Set directory where all the data files are located
data_dir = "chatbot/backend/data_pkl"

def ingest_text_documents():
    # Iterate through all subdirectories in the data_dir
    for dir in os.listdir(data_dir):
        sub_dir_path = os.path.join(data_dir, dir)
        if os.path.isdir(sub_dir_path):  # Check if it's a directory
            # Walk through each subdirectory to find .pkl files
            for root, _, files in os.walk(sub_dir_path):
                print(f"Processing {root}...")
                for filename in files:
                    file_path = os.path.join(root, filename)

                    # 1: Open Pickle Files to access QA-Pairs
                    if filename.endswith(".pkl"):
                        # Load the text chunks from the pickle file
                        with open(file_path, "rb") as f:
                            text_chunks = pickle.load(f)

                        # Embed the text Chunks
                        print("Encoding Text")
                        dense_embeddings, sparse_embeddings = embedding_model.encode_texts(text_chunks)

                        # Prepare the payload for ingestion
                        doc_type = "FAQ" if "faq" in filename.lower() else "Emails"  # Determine doc_source based on filename
                        data = [
                            [doc_type] * len(text_chunks), # doc_name
                            [dir] * len(text_chunks),  # Use the subdirectory name as doc_source
                            text_chunks, # text
                            dense_embeddings,  # Dense embeddings
                            embedding_model.convert_sparse_embeddings(sparse_embeddings),  # payload sparse embeddings
                        ]
                        print("Ingesting Data")
                        # Ingest the original email attachment into the vector database via API
                        try:
                            vector_db.batch_ingestion(data)
                            print(f"Successfully ingested data from {filename}")
                        except Exception as e:
                            print(f"Failed to ingest data from {filename}: {str(e)}")

                    # 2: Upload the mail original documents into the FileStorage
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
    print("Ingesting text documents...")
    ingest_text_documents()


