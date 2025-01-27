# flake8: noqa

import chromadb
import json
import os
from dotenv import load_dotenv
from pathlib import Path
from .read_data import get_clean_data

# Initialise environment variables from root directory
root_dir = Path(__file__).resolve().parent.parent.parent
load_dotenv(dotenv_path=root_dir / ".env")
EMAIL_DOCUMENT_ID = os.getenv("EMAIL_DOCUMENT_ID")
FAQ_DOCUMENT_ID = os.getenv("FAQ_DOCUMENT_ID")

def initialize_db():
    """
    Initialize and populate the ChromaDB vector database with FAQ and email
    data.

    This function performs the following steps:
    1. Creates a new ChromaDB client and collection
    2. Retrieves and processes FAQ and email data from JSON files
    3. Inserts the processed documents into the ChromaDB collection

    Returns:
        chromadb.Collection: Initialized ChromaDB collection containing all
        documents
    """
    print("Initialising vector database...")
    chroma_client = chromadb.Client()
    collection = chroma_client.create_collection(name="iep_chroma_db")
    documents = []
    all_ids = []

    # Fetch and clean data from source
    print("Inserting data...")
    base_path = os.path.join("chatbot", "backend", "database", "data")

    # Process both email and FAQ data
    get_clean_data(EMAIL_DOCUMENT_ID, "email")
    get_clean_data(FAQ_DOCUMENT_ID, "faq")

    # Load and process JSON files
    files = ['FAQ_data.json', 'email_data.json']

    for file in files:
        path = os.path.join(base_path, file)

        with open(path, 'r') as f:
            data = json.load(f)

        for i, item in enumerate(data):
            # Extract QA pairs and their IDs
            if 'QA_pair' in item and 'Subject' in item:
                documents.append(f"{item['QA_pair']}")
                all_ids.append(item['id'])

    # Insert processed documents into ChromaDB collection
    collection.upsert(
        ids=all_ids,
        documents=documents,
    )
    print("Vector database created!")
    return collection


def query_db(collection, query, n_results=2):
    """
    Query the ChromaDB collection for similar documents.

    Args:
        collection (chromadb.Collection): The ChromaDB collection to query
        query (str): The search query text
        n_results (int, optional): Number of results to return. Defaults to 2

    Returns:
        dict: Query results containing matched documents and their IDs
    """
    results = collection.query(query_texts=[query], n_results=n_results)
    return results

# Global collection instance for singleton pattern
global_collection = None


def get_global_collection():
    """
    Get or initialise the global ChromaDB collection instance.

    Implements a singleton pattern to ensure only one database connection
    is maintained throughout the application lifecycle.

    Returns:
        chromadb.Collection: The global ChromaDB collection instance
    """
    global global_collection
    if global_collection is None:
        global_collection = initialize_db()
    return global_collection


def view_collection(collection):
    """
    Display all documents in the ChromaDB collection for debugging purposes.

    Args:
        collection (chromadb.Collection): The ChromaDB collection to view

    Prints:
        - Document content
        - Document ID
        For each document in the collection
    """
    print("Querying collection...")

    # retrieve all the IDs in the collection
    results = collection.query(
        query_texts=[""],  # empty query to fetch all documents
        n_results=100  # number of results to return
    )

    # Display the retrieved data
    for i, document in enumerate(results['documents']):
        print(f"Document {i+1}: {document}")
        print(f"ID: {results['ids'][i]}")
        print()
