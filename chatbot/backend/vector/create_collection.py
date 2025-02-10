from pymilvus import (
    utility,
    CollectionSchema, DataType, FieldSchema, Collection
)

COLLECTION_NAME = "image_vector_index"

AUTO_ID = FieldSchema(
    name="auto_id",
    dtype=DataType.INT64,
    is_primary=True,
    auto_id=True
)

DOC_ID = FieldSchema(
    name="doc_id",
    dtype=DataType.VARCHAR,
    max_length=500
)

DOC_SOURCE = FieldSchema(
    name="doc_source",
    dtype=DataType.VARCHAR,
    max_length=1000,
    default_value="NA"
)

### TEXT FEATURES

TEXT = FieldSchema(
    name="text",
    dtype=DataType.VARCHAR,
    max_length=50000,
    default_value=""
)

TEXT_DENSE_EMBEDDING = FieldSchema(
    name="text_dense_embedding",
    dtype=DataType.FLOAT_VECTOR,
    dim=1024
)

TEXT_SPARSE_EMBEDDING = FieldSchema(
    name="text_sparse_embedding",
    dtype=DataType.SPARSE_FLOAT_VECTOR
)

### IMAGE FEATURES

DESCRIPTION = FieldSchema(
    name="description",
    dtype=DataType.VARCHAR,
    max_length=5000,
    default_value=""
)

DESCRIPTION_EMBEDDING = FieldSchema(
    name="description_embedding",
    dtype=DataType.FLOAT_VECTOR,
    dim=1024
)

IMAGE_EMBEDDING = FieldSchema(
    name="image_embedding",
    dtype=DataType.FLOAT_VECTOR,
    dim=768 # Image embedding dim
)

### DEFINING THE SCHEMA

SCHEMA = CollectionSchema(
    fields=[AUTO_ID, DOC_ID, DOC_SOURCE, TEXT, TEXT_DENSE_EMBEDDING, TEXT_SPARSE_EMBEDDING, DESCRIPTION, DESCRIPTION_EMBEDDING, IMAGE_EMBEDDING],
    description="Schema for indexing documents and images",
    enable_dynamic_field=True
)

def create_collection(collection_name, schema):
    # Check if the collection exists
    if utility.has_collection(collection_name):
        print(f"Collection '{collection_name}' already exists")
    else:
        # Create the collection
        return Collection(name=collection_name, schema=schema, using='default', shards_num=2)

def drop_collection(collection_name):
    # Check if the collection exists
    if utility.has_collection(collection_name):
        collection = Collection(name=collection_name)
        # Release the collection
        collection.release()
        # Drop the collection if it exists
        utility.drop_collection(collection_name)
        print(f"Collection '{collection_name}' has been dropped")
    else:
        print(f"Collection '{collection_name}' does not exist")