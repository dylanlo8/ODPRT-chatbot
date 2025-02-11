from pymilvus import Collection

def create_all_indexes(collection: Collection) -> Collection:
    # dense embeddings index
    collection.create_index(
        field_name="text_dense_embedding",
        index_params={
            "metric_type": "COSINE",
            "index_type": "HNSW",
            "params": {
                "M": 5,
                "efConstruction": 512
            }
        },
        index_name="dense_embeddings_index"
    )
    
    print("Dense embeddings index created")

    # sparse embeddings index
    collection.create_index(
        field_name="text_sparse_embedding",
        index_params={
            "metric_type": "IP",
            "index_type": "SPARSE_INVERTED_INDEX",
            "params": {
                "drop_ratio_build": 0.2
            }
        },
        index_name="sparse_embeddings_index"
    )

    print("Sparse embeddings index created")

    # description embeddings index
    collection.create_index(
        field_name="description_embedding",
        index_params={
            "metric_type": "COSINE",
            "index_type": "HNSW"
        },
        index_name="description_embedding_index"
    )
    
    print("description_embedding index created")

    # sparse embeddings index
    collection.create_index(
        field_name="image_embedding",
        index_params={
            "metric_type": "COSINE",
            "index_type": "HNSW",
        },
        index_name="image_embedding_index"
    )
    
    print("image_embedding index created")
    # load
    collection.load()
    print("Collection loaded")

    return collection