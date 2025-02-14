import extract_msg

def read_email(
    email_path: str
):
    """
    read email from path

    Args:
        email_path (str): email path
    """
    msg = extract_msg.Message(email_path)
    return msg.body
    
def clean_email(
    email_thread: str
) -> str:
    """
    clean email thread using regex/nlp techniques

    Args:
        email_thread (str): email thread
        
    Returns:
        cleaned_email (str): cleaned email thread
    """
    pass