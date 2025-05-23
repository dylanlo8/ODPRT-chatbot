import os

from dotenv import load_dotenv
from pymilvus import utility, connections, Collection, AnnSearchRequest, RRFRanker
from tqdm import tqdm

from chatbot.backend.services.vector_db.schema import SCHEMA
from chatbot.backend.services.vector_db.index import create_all_indexes
from chatbot.backend.services.models.embedding_model import embedding_model
from chatbot.backend.services.logger import logger

load_dotenv(override=True)


class VectorDB:
    def __init__(self, collection_name):
        # Establish a connection to Zillis
        self.endpoint = os.getenv("ZILLIS_ENDPOINT")
        self.token = os.getenv("ZILLIS_TOKEN")
        self.logger = logger
        connections.connect(uri=self.endpoint, token=self.token)

        # Checking if collection was already created
        if utility.has_collection(collection_name):
            print(f"Collection '{collection_name}' already exists")
            self.collection = Collection(name=collection_name)
        else:
            print("Initialising Collection")
            # Create the collection
            self.collection = Collection(
                name=collection_name, schema=SCHEMA, using="default", shards_num=2
            )

            # Creating index for the collection
            self.collection = create_all_indexes(self.collection)

        # Load embedding model
        self.embedding_model = embedding_model

        self.collection_name = collection_name

    def insert(self, data):
        """
        Inserts data into the collection.

        Args:
            data (Any): The data to be inserted into the collection.

        Returns:
            None
        """
        self.collection.insert(data)
        self.collection.load()

    def hybrid_search(self, query: str) -> str:
        """
        Performs a hybrid search on the collection using dense and sparse embeddings.

        Args:
            query (str): The query string to search for.

        Returns:
            str: A formatted string containing the search results.
        """
        # Get query embedding
        dense_embedding, sparse_embedding = self.embedding_model.encode_texts([query])

        # New hybrid search implementation
        search_results = self.collection.hybrid_search(
            reqs=[
                AnnSearchRequest(
                    data=dense_embedding,  # content vector embedding
                    anns_field="text_dense_embedding",
                    param={"metric_type": "COSINE"},
                    limit=3,
                ),
                AnnSearchRequest(
                    data=self.embedding_model.convert_sparse_embeddings(
                        sparse_embedding
                    ),  # keyword vector embedding
                    anns_field="text_sparse_embedding",
                    param={"metric_type": "IP"},
                    limit=3,
                ),
            ],
            output_fields=["doc_id", "text", "doc_source"],
            # using RRFRanker here for reranking
            rerank=RRFRanker(),
            limit=3,
        )

        hits = search_results[0]

        context = []
        # TODO: Modify the context
        for res in hits:
            doc_source = res.doc_source
            text = res.text
            context.append(f"Source Document: {doc_source} \n Text: {text}")
            # self.logger.info(f"Doc_source: {res.doc_source}")
            # self.logger.info(f"Context: {text}")

        return "\n\n".join(context), context

    def drop_collection(self):
        """
        Drops the collection if it exists.

        Returns:
            None
        """
        # Check if the collection exists
        if utility.has_collection(self.collection_name):
            collection = Collection(name=self.collection_name)

            # Release the collection
            collection.release()

            # Drop the collection if it exists
            utility.drop_collection(self.collection_name)
            print(f"Collection '{self.collection_name}' has been dropped")
            self.collection_name = None
        else:
            print(f"Collection '{self.collection_name}' does not exist")

    def batch_ingestion(self, data):
        """
        Performs batch ingestion of data into the collection.

        Args:
            data (Any): The data to be ingested.

        Returns:
            None
        """
        batch_size = 100
        total_elements = len(data)  # Ensure batching considers the number of records
        total_batches = (total_elements + batch_size - 1) // batch_size

        # Using tqdm to create a progress bar
        for start in tqdm(
            range(0, total_elements, batch_size),
            total=total_batches,
            desc="Ingesting batches",
        ):
            end = min(start + batch_size, total_elements)
            batch = data[start:end]  # Slice batch correctly

            self.collection.insert(batch)  # Insert batch into collection

    def delete_data(self, field: str, match_results: list[str]):
        """
        Deletes entries from the collection where the specified field matches any value in match_results.

        Args:
            field (str): The field to match against.
            match_results (list[str]): A list of values to match for deletion.

        Returns:
            Any: The result of the delete operation.
        """
        """
        Delete entries from Milvus where 'field' matches any value in 'match_results'.
        """

        # Convert list to Milvus-compatible expression
        match_list = ", ".join(f"'{item}'" for item in match_results)
        delete_expr = f"{field} in [{match_list}]"  

        # Execute delete operation
        delete_result = self.collection.delete(delete_expr)
        
        return delete_result

vector_db = VectorDB(collection_name="odprt_index")
