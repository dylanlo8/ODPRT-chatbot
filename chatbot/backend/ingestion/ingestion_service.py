import os
import requests
from chatbot.backend.services.models.models import vlm
from chatbot.backend.services.models.embedding_model import embedding_model
from chatbot.backend.services.vector_db.db import vector_db

class IngestionService:
    def ingest_images(self, image_paths):
        """
        Ingests image data into the vector database.

        Steps:
        1. Generate image summaries using the VLM model.
        2. Encode the summaries to generate dense and sparse embeddings.
        3. Prepare the data for ingestion, including metadata and embeddings.
        4. Batch ingest the data into the vector database.
        """
        # Step 1: Generate image summaries
        image_summaries = vlm.generate_image_summaries(image_paths)

        # Step 2: Generate dense and sparse embeddings for the summaries
        dense_embeddings, sparse_embeddings = embedding_model.encode_texts(image_summaries)

        # Step 3: Prepare the data for ingestion
        data = [
            ["Images"] * len(image_paths),  # Assuming all images are from the same source,
            image_paths,  # Assuming all images are from the same source
            image_summaries,
            dense_embeddings,
            embedding_model.convert_sparse_embeddings(sparse_embeddings),
        ]

        # Step 4: Ingest the data into the vector database
        try:
            vector_db.batch_ingestion(data)
            print("Data ingested successfully")
        except Exception as e:
            print(f"Failed to ingest data: {str(e)}")

    def ingest_texts(self, text_chunks, doc_source, doc_type):
        """
        Ingests text data into the vector database.

        Steps:
        1. Encode the provided text chunks to generate dense and sparse embeddings.
        2. Prepare the data for ingestion, including metadata and embeddings.
        3. Batch ingest the data into the vector database.
        """
        # Embed the text Chunks
        print("Encoding Text")
        dense_embeddings, sparse_embeddings = embedding_model.encode_texts(text_chunks)

        # Prepare the data for ingestion
        data = [
            [doc_type] * len(text_chunks),  # doc_name
            [doc_source] * len(text_chunks),  # doc_source (e.g. "Agreement101", "Contract101")
            text_chunks,  # text
            dense_embeddings,  # Dense embeddings
            embedding_model.convert_sparse_embeddings(sparse_embeddings),  # payload sparse embeddings
        ]

        try:
            vector_db.batch_ingestion(data)
            print(f"Successfully ingested data from {doc_source}")
        except Exception as e:
            print(f"Failed to ingest data from {doc_source}: {str(e)}")
