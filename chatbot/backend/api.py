"""
This module defines the main FastAPI application for the chatbot backend.
It includes middleware and routers for various services such as file storage, chat, vector database, and more.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from chatbot.backend.services.file_storage.buckets_api import buckets_router
from chatbot.backend.services.chat_history.sql_db_api import (
    messages_router,
    conversations_router,
    users_router,
    dashboard_router
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

# Add CORS middleware to allow cross-origin requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins; adjust as needed for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers for file storage services
app.include_router(buckets_router)

# Include routers for conversation history services
app.include_router(messages_router)
app.include_router(conversations_router)
app.include_router(users_router)

# Include router for dashboard analytics
app.include_router(dashboard_router)

# Include router for chat-related endpoints
app.include_router(chat_router)

# Include router for vector database operations
app.include_router(vector_db_router)

# Include router for document processing API
app.include_router(document_parser_router)
# app.include_router(faq_parser_router)
# app.include_router(email_processor_router)

# Include router for ingestion API
app.include_router(ingestion_router)

# Include router for topic modeling API
app.include_router(simple_tm_router)

if __name__ == "__main__":
    import uvicorn  # ASGI server for running FastAPI applications

    uvicorn.run(app, host="0.0.0.0", port=8000)  # Run the application on port 8000
