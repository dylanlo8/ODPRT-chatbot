from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from chatbot.backend.services.file_storage.buckets_api import buckets_router
from chatbot.backend.services.chat_history.sql_db_api import (
    messages_router,
    conversations_router,
    users_router,
)
from chatbot.backend.services.vector_db.db_api import vector_db_router
from chatbot.backend.inference.inference_api import chat_router
from chatbot.backend.document_parser.doc_parsing_api import document_parser_router
from chatbot.backend.ingestion.ingestion_api import ingestion_router
from chatbot.backend.topicmodel.topic_model_api import simple_tm_router

# ==========================
# FastAPI Application
# ==========================
app = FastAPI()

app.add_middleware(  # {{ edit_2 }}
    CORSMiddleware,
    allow_origins=["*"],  # Adjust this as needed for your use case
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# File Storage
app.include_router(buckets_router)

# Conversation History
app.include_router(messages_router)
app.include_router(conversations_router)
app.include_router(users_router)

# Chat
app.include_router(chat_router)

# Vector Database
app.include_router(vector_db_router)

# Document Processing API
app.include_router(document_parser_router)
# app.include_router(faq_parser_router)
# app.include_router(email_processor_router)

# Ingestion API
app.include_router(ingestion_router)

# topic modeling
app.include_router(simple_tm_router)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
