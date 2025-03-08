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
    ):
        """
        maps multiple qa pairs to topics using batch embedding

        args:
            qa_pairs (list): list of question-answer pairs
            threshold (float): minimum similarity score required

        returns:
            list: list of best matching topics for each qa pair
        """
        # batch embed all qa pairs
        qa_embeddings = self.embedding_model.embed_documents(qa_pairs)

        # topic matrix
        topic_embeddings_matrix = np.array(
            [self.topic_embeddings[desc] for desc in self.topic_desc_list]
        )

        results = []
        for i, qa_embedding in enumerate(qa_embeddings):
            qa_array = np.array([qa_embedding]).reshape(1, -1)

            # calculate all similarities
            similarities = cosine_similarity(qa_array, topic_embeddings_matrix)[0]

            # get index of highest similarity
            best_index = np.argmax(similarities)
            best_topic = self.topic_desc_list[best_index]
            max_similarity = similarities[best_index]

            # apply threshold chec
            if max_similarity < threshold:
                self.logger.info(
                    f"no topic found for {qa_pairs[i]} with similarity {round(max_similarity, 2)}"
                )
                results.append("no topic found")
            else:
                results.append(best_topic)

        return results


simple_tm = SimpleTopicModel()
