import yaml
import numpy as np

from concurrent.futures import ThreadPoolExecutor
from sklearn.metrics.pairwise import cosine_similarity

from chatbot.backend.services.logger import logger
from chatbot.backend.services.models.embedding_model import embedding_model


class SimpleTopicModel:
    def __init__(
        self,
        embedding_model=embedding_model,
        topics_path: str = "chatbot/backend/configs/topics.yml",
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

    def _map_one_topic(
        self,
        qa_pair: str,
    ):
        """
        uses cosine similarity to map a user's question-answer pair (from history) to the most relevant topic

        Args:
            qa_pair (str): question-answer pair

        Returns:
            best_topic (str): the topic that best matches the qa_pair
        """
        # generate embedding for the qa_pair
        qa_embedding = self.embedding_model.embed_documents([qa_pair])[0]
        qa_array = np.array([qa_embedding])

        # track the highest similarity and corresponding topic
        max_similarity = -1
        best_topic = ""

        # optimize by pre-computing all similarities at once
        for topic_desc, topic_embedding in self.topic_embeddings.items():
            topic_array = np.array([topic_embedding])
            similarity = cosine_similarity(qa_array, topic_array)[0][0]

            # keep track of the highest similarity
            if similarity > max_similarity:
                max_similarity = similarity
                best_topic = topic_desc

        return best_topic

    def map_all_topics(
        self,
        qa_pairs: list,
    ):
        """
        calls `_map_one_topic` in parallel to find the best matching topic for each QA pair

        Args:
            qa_pairs (list): list of question-answer pairs

        Returns:
            list: list of best matching topics for each QA pair
        """
        # use threadpoolexecutor for parallel processing
        with ThreadPoolExecutor() as executor:
            # map each qa_pair to topics in parallel
            results = list(executor.map(self._map_one_topic, qa_pairs))

        return results


simple_tm = SimpleTopicModel()
