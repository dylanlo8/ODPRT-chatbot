import os
import logging
from supabase import create_client, Client
from uuid import uuid4
from datetime import datetime

url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(url, key)

# Checks if  auser exists in the database
def check_user_exists(uuid: str) -> dict:
    """
    Check if a user exists in the database.

    Args:
        uuid (str): The UUID of the user.

    Returns:
        dict: API response indicating whether the user exists.
    """
    try:
        response = supabase.table("users").select("*").eq("user_id", uuid).execute()
        if response.data:
            return {"exists": True}
        else:
            return {"exists": False}
    except Exception as exception:
        logging.error(f"Error checking user existence: {exception}")
        return {"error": str(exception)}

# Insert a new user
def insert_user(uuid: str, faculty: str) -> dict:
    """
    Insert a new user into the users table.

    Args:
        uuid (str): The name of the user.

    Returns:
        dict: API response after inserting the user.
    """
    try:
        response = supabase.table("users").insert([{"user_id": uuid, "faculty": faculty}]).execute()
        return response
    except Exception as exception:
        logging.error(f"Error inserting user: {exception}")
        return {"error": str(exception)}
    
def insert_message(message: dict) -> dict:
    """
    Bulk Insertion of Messages

    Args:
        messages (list[dict]): A list of dictionaries containing the messages to insert

    Returns:
        dict: API response after inserting the messages
    """

    try:
        update_conversation_timing(message['conversation_id'])
        response = supabase.table("messages").insert([message]).execute()
        return response
    except Exception as exception:
        logging.error(f"Error inserting message: {exception}")
        return exception
    
# Bulk Insertion of Conversations
def insert_conversation(conversation: dict) -> dict:
    """
    Bulk Insertion of Conversations

    Args:
        conversation ([dict]): A dictionary containing the conversations to insert

    Returns:
        dict: API response after inserting the conversations
    """
    try:
        response = supabase.table("conversations").insert([conversation]).execute()
        return response
    except Exception as exception:
        return exception

def get_user_conversations(user_id: str) -> dict:
    """
    Retrieve all conversations for a specific user. Sorted by created_at in descending order.
    
    Args:
        user_id (str): The UUID of the user
        
    Returns:
        dict: API response containing the conversations
    """
    try:
        
        # Retrieve the conversations
        response = (
            supabase.table("conversations")
            .select("*")
            .eq("user_id", user_id)
            .order("updated_at", desc=True) # Sort by updated_at in descending order
            .execute()
        )
        return response
    except Exception as exception:
        return exception

def delete_conversation(conversation_id: str) -> dict:
    """
    Delete a specific conversation.
    
    Args:
        conversation_id (str): The UUID of the conversation
    
    Returns:
        dict: API response after deleting the conversation
    """
    try:            
        response = (
            supabase.table("conversations")
            .delete()
            .eq("conversation_id", conversation_id)
            .execute()
        )
        return response
    except Exception as exception:
        return exception

# Querying Conversation and messages
def get_messages(conversation_id: str) -> dict:
    """
    Retrieve all messages for a specific conversation.
    
    Args:
        conversation_id (str): The UUID of the conversation
        
    Returns:
        dict: API response containing the messages
    """
    try:
        response = (
            supabase.table("messages")
            .select("*")
            .eq("conversation_id", conversation_id)
            .order("created_at", desc=False)
            .execute()
        )
        return response
    except Exception as exception:
        return exception
    
# Updating conversation feedback and ratings

def update_conversation_rating(conversation_id: str, rating: int, text: str) -> dict:
    """
    Update the feedback for a specific conversation.
    
    Args:
        conversation_id (str): The UUID of the conversation
        feedback (int): 1 to 5 star ratings for the conversation
        text (str): Feedback text
        
    Returns:
        dict: API response after updating the feedback
    """
    try:
        response = (
            supabase.table("conversations")
            .update({"rating": rating, "feedback": text})
            .eq("conversation_id", conversation_id)
            .execute()
        )
        return response
    except Exception as exception:
        return exception
    
def update_conversation_timing(conversation_id: str) -> dict:
    """
    Update the conversation timing for a specific conversation.
    
    Args:
        conversation_id (str): The UUID of the conversation
        
    Returns:
        dict: API response after updating the conversation timing
    """
    try:
        response = (
            supabase.table("conversations")
            .update({"updated_at": "now()"})
            .eq("conversation_id", conversation_id)
            .execute()
        )
        return response
    except Exception as exception:
        return exception
    
def update_message_useful(message_id: str, is_useful: bool) -> dict:
    """
    Update the usefulness of a specific message.
    
    Args:
        message_id (str): The UUID of the message
        is_useful (bool): True if the message is useful, False otherwise
        
    Returns:
        dict: API response after updating the message usefulness
    """
    try:
        response = (
            supabase.table("messages")
            .update({"is_useful": is_useful})
            .eq("message_id", message_id)
            .execute()
        )
        return response
    except Exception as exception:
        return exception
    
def update_conversation_title(conversation_id: str, title: str) -> dict:
    """
    Update the title of a specific conversation.
    
    Args:
        conversation_id (str): The UUID of the conversation
        title (str): The new title for the conversation
        
    Returns:
        dict: API response after updating the conversation title
    """
    try:
        response = (
            supabase.table("conversations")
            .update({"conversation_title": title})
            .eq("conversation_id", conversation_id)
            .execute()
        )
        return response
    except Exception as exception:
        return exception
    
def fetch_dashboard_statistics(
    start_date: str = "01-01-2024",  # dd-mm-yyyy
    end_date: str = "31-12-2025"
) -> dict:
    """
    Calls the Supabase RPC function to fetch dashboard statistics as a JSON object.

    Parameters:
        start_date (str): Start date in 'dd-mm-yyyy' format.
        end_date (str): End date in 'dd-mm-yyyy' format.

    Returns:
        dict: JSON result from fetch_conversation_stats_json() SQL function.
    """
    try:
        # Parse using dd-mm-yyyy format
        start_dt = datetime.strptime(start_date, "%Y-%m-%d")
        end_dt = datetime.strptime(end_date, "%Y-%m-%d")

        # Format into proper timestamp strings
        start_timestamp = start_dt.strftime("%Y-%m-%d 00:00:00")
        end_timestamp = end_dt.strftime("%Y-%m-%d 23:59:59")

        # Call Supabase RPC function
        response = supabase.rpc("fetch_conversation_stats_json", {
            "start_date": start_timestamp,
            "end_date": end_timestamp
        }).execute()

        return response.data if hasattr(response, "data") else response
    except Exception as e:
        print("Error fetching dashboard statistics:", e)
        return {"error": str(e)}
    
def update_conversation_topic(conversation_id: str, topic: str) -> dict:
    """
    Update the topic of a specific conversation.

    Args:
        conversation_id (str): The UUID of the conversation.
        topic (str): The new topic for the conversation.

    Returns:
        dict: API response after updating the conversation topic.
    """
    try:
        response = (
            supabase.table("conversations")
            .update({"topic": topic})
            .eq("conversation_id", conversation_id)
            .execute()
        )
        return response
    except Exception as exception:
        logging.error(f"Error updating conversation topic: {exception}")
        return {"error": str(exception)}

def update_conversation_intervention(conversation_id: str) -> dict:
    """
    Update the intervention timing of a specific conversation.

    Args:
        conversation_id (str): The UUID of the conversation.

    Returns:
        dict: API response after updating the conversation intervention timing.
    """
    try:
        response = (
            supabase.table("conversations")
            .update({"intervention_required": True})
            .eq("conversation_id", conversation_id)
            .execute()
        )
        return response
    except Exception as exception:
        logging.error(f"Error updating conversation intervention timing: {exception}")
        return {"error": str(exception)}
