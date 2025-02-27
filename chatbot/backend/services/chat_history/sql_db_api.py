from fastapi import FastAPI, APIRouter, HTTPException
from pydantic import BaseModel
from chatbot.backend.services.chat_history.sql_db import (
    bulk_insert_messages,
    bulk_insert_conversations,
    get_user_conversations,
    delete_conversation,
    get_conversation_messages,
    update_conversation_rating,
)
# ==========================
# Pydantic Models
# ==========================
class Message(BaseModel):
    content: dict

class Conversation(BaseModel):
    content: dict

class Rating(BaseModel):
    rating: int  # conversation_id is now passed in the URL

# ==========================
# FastAPI Routers
# ==========================
messages_router = APIRouter(prefix="/messages", tags=["Messages"])
conversations_router = APIRouter(prefix="/conversations", tags=["Conversations"])
users_router = APIRouter(prefix="/users", tags=["Users"])

# Messages Routes
@messages_router.post("/bulk-insert")
def bulk_insert_messages_route(messages: list[Message]):
    response = bulk_insert_messages([msg.content for msg in messages])
    return response

# Conversations Routes
@conversations_router.post("/bulk-insert")
def bulk_insert_conversations_route(conversations: list[Conversation]):
    response = bulk_insert_conversations([conv.content for conv in conversations])
    return response

@conversations_router.get("/{conversation_id}/messages")
def get_conversation_messages_route(conversation_id: str):
    response = get_conversation_messages(conversation_id)
    return response

@conversations_router.delete("/{conversation_id}")
def delete_conversation_route(conversation_id: str):
    response = delete_conversation(conversation_id)
    return response

@conversations_router.put("/{conversation_id}/rate")
def update_conversation_rating_route(conversation_id: str, rating: Rating):
    response = update_conversation_rating(conversation_id, rating.rating)
    return response

# Users Routes
@users_router.get("/{user_id}/conversations")
def get_user_conversations_route(user_id: str):
    response = get_user_conversations(user_id)
    return response

