from pymilvus import utility, connections, Collection, AnnSearchRequest, RRFRanker
from .schema import SCHEMA
from .index import create_all_indexes
from chatbot.backend.services.embedding_model import embedding_model
from tqdm import tqdm
from dotenv import load_dotenv
import os

class VectorDB:
    def __init__(self, collection_name):
        load_dotenv()

        # Establish a connection to Zillis
        self.endpoint = os.getenv('ZILLIS_ENDPOINT')
        self.token = os.getenv('ZILLIS_TOKEN')
        connections.connect(uri=self.endpoint, token=self.token)

        # Checking if collection was already created
        if utility.has_collection(collection_name):
            print(f"Collection '{collection_name}' already exists")
            self.collection = Collection(name=collection_name) 
        else:
            print("Initialising Collection")
            # Create the collection
            self.collection = Collection(name=collection_name, schema=SCHEMA, using='default', shards_num=2)

            # Creating index for the collection
            self.collection = create_all_indexes(self.collection)
        
        # Load embedding model
        self.embedding_model = embedding_model

        self.collection_name = collection_name

    def insert(self, data):
        self.collection.insert(data)
        self.collection.load()

    def image_hybrid_search(self, query: str) -> str:
        # Get query embedding
        query_embedding = self.embedding_model.encode_texts(query)[0]
        
        search_results = self.collection.hybrid_search(
                reqs=[
                    AnnSearchRequest(
                        data=[query_embedding],  # content vector embedding
                        anns_field='description_embedding',  # content vector field
                        param={"metric_type": "COSINE", "params": {"M": 64, "efConstruction": 512}}, 
                        limit=3
                    ),
                    AnnSearchRequest(
                        data=[query_embedding],  # keyword vector embedding
                        anns_field='image_embedding',  # keyword vector field
                        param={"metric_type": "COSINE", "params": {"M": 64, "efConstruction": 512}}, 
                        limit=3
                    )
                ],
                output_fields=['doc_id', 'description'],
                # using RRFRanker here for reranking
                rerank=RRFRanker(),
                limit=1
            )
        
        hits = search_results[0]
        
        context = []
        for res in hits:
            doc_id = res.doc_id
            description = res.description
            context.append(f"Doc_id: {doc_id} \n Description: {description}")
        
        return "\n\n".join(context)
            
    def drop_collection(self):
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
        batch_size = 100
        total_elements = len(data)  # Ensure batching considers the number of records
        total_batches = (total_elements + batch_size - 1) // batch_size

        # Using tqdm to create a progress bar
        for start in tqdm(range(0, total_elements, batch_size), 
                        total=total_batches,
                        desc="Ingesting batches"):
            end = min(start + batch_size, total_elements)
            batch = data[start:end]  # Slice batch correctly

            self.collection.insert(batch)  # Insert batch into collection
