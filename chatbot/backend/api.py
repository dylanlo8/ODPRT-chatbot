from fastapi import FastAPI
from chatbot.backend.services.file_storage.buckets_api import buckets_router
from chatbot.backend.services.chat_history.sql_db_api import messages_router, conversations_router, users_router
from chatbot.backend.services.vector_db.db_api import vector_db_router
from chatbot.backend.inference.inference_api import chat_router

# ==========================
# FastAPI Application
# ==========================
app = FastAPI()

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

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)