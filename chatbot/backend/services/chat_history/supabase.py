import os
from supabase import create_client, Client

url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(url, key)

# Bulk Insertion of Messages
def bulk_insert_messages(messages: list[dict]) -> dict:
    try:
        response = supabase.table("messages").insert(messages).execute()
        return response
    except Exception as exception:
        return exception
    
# Bulk Insertion of Conversations
def bulk_insert_conversations(conversations: list[dict]) -> dict:
    try:
        response = supabase.table("conversations").insert(conversations).execute()
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
        # Each time a user's conversations are retrieved, the old conversations are cleaned up
        print(clean_up_old_conversations(user_id))

        # Retrieve the conversations
        response = (
            supabase.table("conversations")
            .select("*")
            .eq("user_id", user_id)
            .order("created_at", desc=True)
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
    # Clean up old conversations if user has more than 10
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
def get_conversation_messages(conversation_id: str) -> dict:
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

def update_conversation_rating(conversation_id: str, rating: int) -> dict:
    """
    Update the feedback for a specific conversation.
    
    Args:
        conversation_id (str): The UUID of the conversation
        feedback (int): 1 to 5 star ratings for the conversation
        
    Returns:
        dict: API response after updating the feedback
    """
    try:
        response = (
            supabase.table("conversations")
            .update({"rating": rating})
            .eq("conversation_id", conversation_id)
            .execute()
        )
        return response
    except Exception as exception:
        return exception