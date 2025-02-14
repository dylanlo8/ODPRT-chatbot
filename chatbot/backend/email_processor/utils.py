import extract_msg
import os

from typing import Optional

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
    # TODO: implement cleaning
    return email_thread

def get_all_emails(
    directory: str = 'docs/emails'
):
    """
    get all emails from directory

    Args:
        directory (Optional[str]): directory to get emails from
        
    Returns:
        emails (List[str]): list of emails
    """
    emails = []
    for child_dir in os.listdir(directory):
        if not os.path.isdir(os.path.join(directory, child_dir)):
            continue
        for email in os.listdir(os.path.join(directory, child_dir)):
            if not email.endswith('.msg'):
                continue
            email_path = os.path.join(directory, child_dir, email)
            cleaned_email = clean_email(read_email(email_path=email_path))
            emails.append(cleaned_email)
    return emails