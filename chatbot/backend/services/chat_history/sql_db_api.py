from fastapi import FastAPI, APIRouter, HTTPException
from pydantic import BaseModel
from chatbot.backend.services.chat_history.sql_db import (
    insert_message,
    insert_conversation,
    get_user_conversations,
    delete_conversation,
    get_messages,
    update_conversation_rating,
)

# ==========================
# Pydantic Models
# ==========================
class Message(BaseModel):
    content: dict

class Conversation(BaseModel):
    content: dict

class Feedback(BaseModel):
    rating: int  # conversation_id is now passed in the URL
    text: str

################################
# FastAPI Routers
################################
messages_router = APIRouter(prefix="/messages", tags=["Messages"])
conversations_router = APIRouter(prefix="/conversations", tags=["Conversations"])
users_router = APIRouter(prefix="/users", tags=["Users"])

################################
# Users Routes
################################
@users_router.get("/{user_id}/conversations")
def get_user_conversations_route(user_id: str):
    response = get_user_conversations(user_id)
    return response

################################
# Conversations Routes
################################
@conversations_router.get("/{conversation_id}/messages")
def get_conversation_messages_route(conversation_id: str):
    response = get_messages(conversation_id)
    return response

@conversations_router.post("insert")
def insert_conversations_route(conversation: Conversation):
    response = insert_conversation([conversation.content])
    return response

@conversations_router.delete("/{conversation_id}")
def delete_conversation_route(conversation_id: str):
    response = delete_conversation(conversation_id)
    return response

@conversations_router.put("/{conversation_id}/feedback")
def update_conversation_rating_route(conversation_id: str, feedback: Feedback):
    response = update_conversation_rating(conversation_id, feedback.rating, feedback.text)
    return response

################################
# Messages Routes
################################
@messages_router.post("/insert")
def insert_messages_route(message: Message):
    response = insert_message([message.content])
    return response

"""
# Sample payload for conversations table
conversation_payload = {
    "conversation_id": "123e4567-e89b-12d3-a456-426614174000", # DEFAULT
    "session_id": "123e4567-e89b-12d3-a456-426614174001", # NEED TO INPUT
    "conversation_title": "Sample Conversation", # NEED TO INPUT
    "created_at": "2025-03-11T10:00:00Z", # DEFAULT
    "updated_at": "2025-03-11T10:00:00Z", # DEFAULT
    "rating": 4,
    "feedback": "This was a helpful conversation."
}

# Sample payload for messages table
message_payload = {
    "message_id": "123e4567-e89b-12d3-a456-426614174002",
    "conversation_id": "123e4567-e89b-12d3-a456-426614174000",
    "sender": "user",
    "text": "Hello, how can I help you?",
    "is_useful": True,
    "created_at": "2025-03-11T10:01:00Z"
}

# Insert sample data into conversations table
response_conversation = supabase.table("conversations").insert([conversation_payload]).execute()
print(response_conversation)

# Insert sample data into messages table
response_message = supabase.table("messages").insert([message_payload]).execute()
print(response_message)
"""