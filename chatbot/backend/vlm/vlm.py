import base64
import requests
from io import BytesIO
from PIL import Image
import os
import numpy as np
import torch
from visual_bge.modeling import Visualized_BGE
from pymilvus import (
    utility,
    CollectionSchema, DataType, FieldSchema, model,
    connections, Collection, AnnSearchRequest, RRFRanker,
)


ENDPOINT = os.getenv('ZILLIS_ENDPOINT')
TOKEN = os.getenv('ZILLIS_TOKEN')
connections.connect(uri=ENDPOINT, token=TOKEN)

# Initialise Hyperbolic API Details
api_key = os.getenv("HYPERBOLIC_API_KEY")
api = "https://api.hyperbolic.xyz/v1/chat/completions"
headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {api_key}",
}

# Embedding Model
embedding_model = Visualized_BGE(model_name_bge="BAAI/bge-base-en-v1.5", model_weight="path:Visualized_base_en_v1.5.pth")
embedding_model.eval()

# Load Image
image_path = "chatbot/backend/vlm/image.png"
img = Image.open(image_path)

# Encode Images for Payload
def encode_image(img):
    buffered = BytesIO()
    img.save(buffered, format="PNG")
    encoded_string = base64.b64encode(buffered.getvalue()).decode("utf-8")
    return encoded_string

base64_img = encode_image(img)

# API payload for generating image summary
payload = {
    "messages": [
        {
            "role": "user",
            "content": [
                {"type": "text", "text": "Generate me a summary of this image?"},
                {
                    "type": "image_url",
                    "image_url": {"url": f"data:image/jpeg;base64,{base64_img}"},
                },
            ],
        }
    ],
    "model": "Qwen/Qwen2-VL-7B-Instruct",
    "max_tokens": 2048,
    "temperature": 0.7,
    "top_p": 0.9,
}

# Get response from VLM
response = requests.post(api, headers=headers, json=payload)

# Extract summary from response
summary = response.json().get("choices", [{}])[0].get("message", {}).get("content", "No summary available")

# Helper function to generate embeddings
def generate_embeddings(image_path, text_summary):
    """Generates embeddings for both image and optional text summary."""
    description_embedding = []
    image_embedding = []

    with torch.no_grad():
        if text_summary and text_summary != "No summary available":
            description_embedding = embedding_model.encode(text=text_summary).tolist()
        
        # Generate embedding for image
        image_embedding = embedding_model.encode(image=image_path).tolist()

    return description_embedding, image_embedding

# Generate embeddings
description_embedding, image_embedding = generate_embeddings(image_path, summary)

# Ingest into Milvus
collection = Collection("image_vector_index")

# Create insert data
insert_data = [
    None,  # auto_id will be generated automatically
    "doc_001",  # doc_id
    "uploaded_image",  # doc_source
    "",  # text (not used here)
    [0.0] * 1024,  # text_dense_embedding placeholder
    [],  # text_sparse_embedding placeholder
    summary if summary != "No summary available" else "",  # description (store empty if no summary)
    description_embedding,  # description_embedding (empty if no summary)
    image_embedding  # image_embedding
]

# Insert into the collection
collection.insert([insert_data])

print(f"Image and summary successfully ingested into Milvus.")
