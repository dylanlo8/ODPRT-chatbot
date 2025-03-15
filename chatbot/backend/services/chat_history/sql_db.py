import os
from supabase import create_client, Client
from datetime import datetime

url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(url, key)

# Bulk Insertion of Messages
def insert_message(message: dict) -> dict:
    """
    Bulk Insertion of Messages

    Args:
        messages (list[dict]): A list of dictionaries containing the messages to insert

    Returns:
        dict: API response after inserting the messages
    """

    try:
        # update_conversation_timing(message["conversation_id"])
        response = supabase.table("messages").insert(message).execute()
        return response
    except Exception as exception:
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
        response = supabase.table("conversations").insert(conversation).execute()
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
    

def clean_up_old_conversations(user_id: str):
    # TODO: Clean up old conversations if user has more than 10
    user_conversations = get_user_conversations(user_id)
    if len(user_conversations.data) > 10:
        # Sort by created_at descending and get conversations to delete
        conversations_to_delete = sorted(
            user_conversations.data,
            key=lambda x: x['updated_at'],
            reverse=True
        )[10:]
        
        # Delete older conversations
        for conv in conversations_to_delete:
            delete_conversation(conv['conversation_id'])
        return {'response': 'success'}
    else:
        return {'response': '<10 conversations, no clean up needed'}

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