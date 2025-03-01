import numpy as np
import torch
from sentence_transformers import SentenceTransformer
from pymilvus import model  # Ensure to import the correct module

from typing import List

class EmbeddingModel:
    def __init__(self):
        self.dense_embedding_model = SentenceTransformer('BAAI/bge-large-en-v1.5')
        self.dense_embedding_model.eval()
        self.sparse_embedding_model = model.sparse.SpladeEmbeddingFunction(
            model_name="naver/splade-cocondenser-ensembledistil",
            device="cpu",
        )

    def batch_encode_dense(self, texts):
        """Generates dense embeddings for texts."""
        description_embeddings = self.dense_embedding_model.encode(texts, normalize_embeddings=True).tolist()
        return description_embeddings

    def batch_encode_sparse(self, texts):
        """Generates sparse embeddings for texts."""
        sparse_embeddings = self.sparse_embedding_model.encode_documents(texts)
        return sparse_embeddings

    def encode_texts(self, texts):
        """Generates both dense and sparse embeddings for texts."""
        dense_embeddings = self.batch_encode_dense(texts)
        sparse_embeddings = self.batch_encode_sparse(texts)
        return dense_embeddings, sparse_embeddings

    def convert_sparse_embeddings(self, sparse_embeddings):
        """Converts sparse embeddings into an ingestable dictionary format."""
        return [
            {j: float(sparse_embeddings[i, j]) for j in sparse_embeddings[[i], :].nonzero()[1].tolist()}
            for i in range(sparse_embeddings.shape[0])
        ]

# Create an instance of the fused model
embedding_model = EmbeddingModel()
