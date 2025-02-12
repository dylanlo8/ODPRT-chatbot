from chatbot.backend.services.vector_db.db import VectorDB
from chatbot.backend.services.models import vlm
from chatbot.backend.services.embedding_model import embedding_model

# Sample ingestion pipeline
print("Initialising vector db")
vector_db = VectorDB("odprt")

# Test drop collection
print("Dropping")
vector_db.drop_collection()

# Test VectorDB Initialisation again
print("Initialising vectordb again")
vector_db = VectorDB("odprt")

# Load images
image_paths = ["34.png", "43.png", "46.png", "160.png", "archi.png"]
image_paths = [f"chatbot/backend/sample_images/{path}" for path in image_paths]

# Test VLM
print("Testing vlm")
image_summaries = vlm.generate_image_summaries(image_paths=image_paths)

# Test Embedding Model Encoding
print("Testing embedding model")
description_embeddings = embedding_model.batch_encode(image_summaries)

# Compile sample data into VectorDB SCHEMA format
# TODO: Consider making a helper function in db class
data = [
    {
        "doc_id": image_paths[i],
        "doc_source": "sample_images",
        "text": "",
        "text_dense_embedding": [0.0] * 1024,  # Placeholder for text dense embedding
        "text_sparse_embedding": [],  # Empty sparse vector
        "description": image_summaries[i],
        "description_embedding": description_embeddings[i],  # Embedding for Image Descriptions
    }
    for i in range(len(image_paths))
]

# Test Batch Ingestion
print("Testing batch ingest")
vector_db.batch_ingestion(data = data)

# Test Hybrid Search
print("Test hybrid")
print(vector_db.image_hybrid_search("Model Architecture"))

