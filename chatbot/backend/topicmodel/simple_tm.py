import yaml
import numpy as np

from sklearn.metrics.pairwise import cosine_similarity

from chatbot.backend.services.logger import logger
from chatbot.backend.services.models.embedding_model import embedding_model


class SimpleTopicModel:
    def __init__(
        self,
        embedding_model=embedding_model,
        topics_path: str = "chatbot/backend/configs/topics.yml",
        max_workers: int = 4,
    ):
        """
        topics.yml file should be structured as follows:
            topics:
                - "desc1"
                - "desc2"
                - "desc3"
                - ...
        """
        self.embedding_model = embedding_model
        self.topics_path = topics_path
        self.max_workers = max_workers
        with open(topics_path, "r") as file:
            yaml_content = yaml.safe_load(file)
            self.topic_descriptions = yaml_content.get("topics", [])
            if not self.topic_descriptions:
                raise ValueError(
                    "no topics found in the provided topics.yml file. need to provide in chatbot/backend/configs!"
                )
        self.logger = logger

        # pre-compute embeddings for all topics
        self.topic_embeddings = self._compute_topic_embeddings()
        self.topic_desc_list = list(self.topic_embeddings.keys())

    def _compute_topic_embeddings(self):
        """
        pre-compute embeddings for all topics to avoid repeated computation

        returns:
            dict: dictionary mapping topic descriptions to their embeddings
        """
        # generate embeddings for all topic descriptions
        embeddings = self.embedding_model.embed_documents(self.topic_descriptions)

        # create dict mapping topic descriptions to their embeddings
        topic_embeddings = {
            desc: embedding
            for desc, embedding in zip(self.topic_descriptions, embeddings)
        }
        return topic_embeddings

    def map_all_topics(
        self,
        qa_pairs: list,
        threshold=0.2,
    ) -> str:
        """
        Maps multiple QA pairs to the most relevant topic using batch embedding.

        Args:
            qa_pairs (list): List of question-answer pairs.
            threshold (float): Minimum similarity score required.

        Returns:
            str: The most relevant topic for the QA pairs, or None if no topic is relevant.
        """
        # Batch embed all QA pairs
        qa_embeddings = self.embedding_model.embed_documents(qa_pairs)

        # Topic matrix
        topic_embeddings_matrix = np.array(
            [self.topic_embeddings[desc] for desc in self.topic_desc_list]
        )

        # Initialize variables to track the best topic and similarity
        best_topic = None
        max_similarity = 0

        for i, qa_embedding in enumerate(qa_embeddings):
            qa_array = np.array([qa_embedding]).reshape(1, -1)

            # Calculate all similarities
            similarities = cosine_similarity(qa_array, topic_embeddings_matrix)[0]

            # Get index of highest similarity
            best_index = np.argmax(similarities)
            candidate_topic = self.topic_desc_list[best_index]
            candidate_similarity = similarities[best_index]

            # Apply threshold check
            if candidate_similarity >= threshold and candidate_similarity > max_similarity:
                best_topic = candidate_topic
                max_similarity = candidate_similarity

        if best_topic:
            return best_topic
        else:
            self.logger.info("No relevant topic found for the provided QA pairs.")
            return None


simple_tm = SimpleTopicModel()
