import torch
from sentence_transformers import SentenceTransformer

class EmbeddingModel:
    def __init__(self):
        self.embedding_model = SentenceTransformer('BAAI/bge-large-en-v1.5')
        self.embedding_model.eval()
    
    def batch_encode(self, texts):
        """Generates dense embeddings for texts."""
        description_embeddings = []

        for text in texts:
            description_embeddings.append(self.__encode_text(text))
        
        return description_embeddings
        
    def __encode_text(self, text):
        """Generates dense embeddings for text."""
        with torch.no_grad():
            # Generate embedding for summary of image           
            description_embedding = self.embedding_model.encode(text, normalize_embeddings=True).tolist()

        return description_embedding

embedding_model = EmbeddingModel()