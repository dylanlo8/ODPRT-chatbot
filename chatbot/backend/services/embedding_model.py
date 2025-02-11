import torch
from visual_bge.modeling import Visualized_BGE

MODEL_PATH = "chatbot/backend/services/Visualized_base_en_v1.5.pth"

class EmbeddingModel:
    def __init__(self):
        self.embedding_model = Visualized_BGE(model_name_bge="BAAI/bge-base-en-v1.5", model_weight=MODEL_PATH)
        self.embedding_model.eval()

    def encode_images_summaries(self, image_summaries, image_paths):
        description_embeddings = []
        image_embeddings = []

        # Generate embeddings
        for i, image_path in enumerate(image_paths):
            description_embedding, image_embedding = self.__encode_image_summary(image_summary=image_summaries[i], image_path=image_path)
            description_embeddings.append(description_embedding)
            image_embeddings.append(image_embedding)
        
        return description_embeddings, image_embeddings
    
    def encode_texts(self, texts):
        """Generates dense embeddings for texts."""
        description_embeddings = []

        for text in texts:
            description_embeddings.append(self.__encode_text(text))
        
        return description_embeddings
    
    def __encode_image_summary(self, image_summary, image_path):
        """Generates dense embeddings for both image and text summary."""
        description_embedding = []
        image_embedding = []

        with torch.no_grad():
            # Generate embedding for summary of image           
            description_embedding = self.embedding_model.encode(text=image_summary).tolist()[0]
            
            # Generate embedding for image
            image_embedding = self.embedding_model.encode(image=image_path).tolist()[0]

        return description_embedding, image_embedding
        
    def __encode_text(self, image_summary):
        """Generates dense embeddings for text."""
        description_embedding = []

        with torch.no_grad():
            # Generate embedding for summary of image           
            description_embedding = self.embedding_model.encode(text=image_summary).tolist()[0]

        return description_embedding

embedding_model = EmbeddingModel()