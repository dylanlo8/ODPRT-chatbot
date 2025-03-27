from fastapi import FastAPI, APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
from chatbot.backend.services.chat_history.sql_db import (
    insert_message,
    insert_conversation,
    get_user_conversations,
    delete_conversation,
    get_messages,
    update_conversation_rating,
    fetch_dashboard_statistics,
    update_conversation_title,
    update_message_useful
)

# ==========================
# Pydantic Models
# ==========================
class MessageContent(BaseModel):
    conversation_id: str
    sender: str
    text: str

class ConversationContent(BaseModel):
    conversation_id: str
    user_id: str
    conversation_title: str
    rating: Optional[int] = None
    feedback: Optional[str] = None

class Feedback(BaseModel):
    rating: int  # conversation_id is now passed in the URL
    text: str

class DateRange(BaseModel):
    start_date: str
    end_date: str

################################
# FastAPI Routers
################################
messages_router = APIRouter(prefix="/messages", tags=["Messages"])
conversations_router = APIRouter(prefix="/conversations", tags=["Conversations"])
users_router = APIRouter(prefix="/users", tags=["Users"])
dashboard_router = APIRouter(prefix="/dashboard", tags=["Dashboard"])

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

@conversations_router.post("/insert")
def insert_conversations_route(conversation: ConversationContent):
    response = insert_conversation(conversation.model_dump())
    return response

@conversations_router.delete("/{conversation_id}")
def delete_conversation_route(conversation_id: str):
    response = delete_conversation(conversation_id)
    return response

@conversations_router.put("/{conversation_id}/feedback")
def update_conversation_rating_route(conversation_id: str, feedback: Feedback):
    response = update_conversation_rating(conversation_id, feedback.rating, feedback.text)
    return response

@conversations_router.put("/{conversation_id}/title")
def update_conversation_title_route(conversation_id: str, title: str):
    response = update_conversation_title(conversation_id, title)
    return response

################################
# Messages Routes
################################
@messages_router.post("/insert")
def insert_messages_route(message: MessageContent):
    response = insert_message(message.model_dump())
    return response


################################
# Dashboard Routes
################################
@dashboard_router.post("/fetch")
def fetch_dashboard_statistics_route(date_range: DateRange):
    response = fetch_dashboard_statistics(
        start_date=date_range.start_date, 
        end_date=date_range.end_date
    )
    return response
@messages_router.put("/{message_id}/useful")
def update_message_useful_route(message_id: str, is_useful: bool):
    response = update_message_useful(message_id, is_useful)
    return response