from fastapi import FastAPI, HTTPException, APIRouter
from pydantic import BaseModel
from chatbot.backend.services.vector_db.db import VectorDB

# ==========================
# Initialize VectorDB instance
# ==========================
vector_db = VectorDB(collection_name="odprt_index")

# ==========================
# Pydantic Models
# ==========================

class InsertData(BaseModel):
    data: list

class SearchQuery(BaseModel):
    query: str

class DropCollection(BaseModel):
    collection_name: str

# ==========================
# FastAPI Router
# ==========================
vector_db_router = APIRouter(prefix="/vector-db")

@vector_db_router.post("/insert-documents/")
async def insert_documents(insert_data: InsertData):
    try:
        vector_db.batch_ingestion(insert_data.data)
        return {"message": "Data inserted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@vector_db_router.post("/hybrid-search/")
async def hybrid_search(search_query: SearchQuery) -> dict:
    try:
        context = vector_db.hybrid_search(search_query.query)
        return {"context": context}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@vector_db_router.delete("/drop-collection/")
async def drop_collection(drop_collection: DropCollection):
    try:
        vector_db.drop_collection()
        return {"message": f"Collection '{drop_collection.collection_name}' dropped successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
