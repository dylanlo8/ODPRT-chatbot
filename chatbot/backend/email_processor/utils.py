import extract_msg
import os
import re


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

def extract_email_attachments(
    email_path: str
):
    """
    read email from path and extract attachments

    Args:
        email_path (str): email path
    """
    files = []
    root_dir = os.path.dirname(os.path.abspath(__file__))
    save_directory = os.path.join(root_dir, 'extracted_attachments')
    os.makedirs(save_directory, exist_ok=True)

    msg = extract_msg.Message(email_path)
    msg.save()

    for attachment in msg.attachments:
        filename = attachment.longFilename or attachment.shortFilename
        filename = filename.replace("/", "_").replace("\\", "_").replace(":", "_")

        file_path = os.path.join(save_directory, filename)

        try:
            attachment.save(customPath=save_directory)
            files.append(file_path)
            print(f"✅ Saved attachment: {file_path}")

        except Exception as e:
            print(f"❌ Error saving {filename}: {e}")

    return files

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
    thread_splitter = r"\n?---+\n?"
    email_threads = re.split(thread_splitter, email_thread.strip())

    cleaned_threads = []

    for thread in email_threads:
        if not thread.strip():
            continue

        thread = re.sub(r"^(From|To|Cc|BCC|Sent|Subject): .*?$", "", thread, flags=re.MULTILINE)

        thread = re.sub(r"(?i)^Message Classification: .*?$", "", thread, flags=re.MULTILINE)

        thread = re.sub(r"(?i)^(Dear|Hi|Hello|Hey)\s+[A-Z][a-z]+,?", "", thread, flags=re.MULTILINE)

        sign_off_pattern = r"""
            (?i)
            \b(Best regards|Regards|Warmest Regards|Sincerely|Thanks|Warm regards|
            Kind regards|Cheers|Yours truly|With appreciation|With thanks|Respectfully|Best )\b
            ,?\s*\n+
            (?:[A-Z][a-z]+(?: [A-Za-z'-]+)*,?\s*(?:[A-Z][a-z]*)?)?
            (?:\s*\(.*?\))?
        """
        thread = re.sub(sign_off_pattern, "", thread, flags=re.VERBOSE | re.MULTILINE)

        signature_pattern = r"""
            (?i)
            (?:[-]{2,}\s*\n)?
            (?:[A-Z][a-z]+(?: [A-Z][a-z]+)*,?\s*(?:[A-Z][a-z]*)?)?
            (?:\s*\(.*?\))?
            (?:\s*\n)?
            (?:.*?::.*\n)+
        """
        thread = re.sub(signature_pattern, "", thread, flags=re.VERBOSE | re.MULTILINE)

        disclaimer_patterns = [
            r"Important: This email is confidential.*?Thank you\.",
            r"If you are not the intended recipient.*?",
            r"This message is intended only for the recipient.*?",
            r"Please delete it if received in error.*?",
        ]
        for pattern in disclaimer_patterns:
            thread = re.sub(pattern, "", thread, flags=re.IGNORECASE | re.DOTALL)

        thread = re.sub(r"(?m)^>+.*$", "", thread)

        thread = re.sub(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b", "", thread)

        thread = re.sub(r"https?://\S+|www\.\S+", "", thread)

        thread = re.sub(r"\b(?:\+?\d{1,3}[-.\s]?)?(?:\(?\d{2,4}\)?[-.\s]?)?\d{3,4}[-.\s]?\d{3,4}\b", "", thread)

        thank_you_patterns = [
            r"(?i)\bThank you\b.*?(\.|\n)",
            r"(?i)\bThanks\b.*?(\.|\n)",
            r"(?i)\bMuch appreciated\b.*?(\.|\n)",
            r"(?i)\bAppreciate it\b.*?(\.|\n)",
            r"(?i)\bWith gratitude\b.*?(\.|\n)",
            r"(?i)\bThank\b.*?(\.|\n)",
        ]
        for pattern in thank_you_patterns:
            thread = re.sub(pattern, "", thread, flags=re.MULTILINE)

        thread = re.sub(r"\s+", " ", thread)
        thread = re.sub(r"[^\x00-\x7F]+", "", thread)

        thread = re.sub(r"[-_]{2,}", "", thread)

        thread = thread.strip()

        if thread:
            cleaned_threads.append(thread)

    return "\n\n---\n\n".join(cleaned_threads)


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

def re_order_email_threads(
        email_thread: str
    ) -> str:
    """Re-order email threads from old to new"""
    thread_splitter = r"(?=From: )"
    emails = re.split(thread_splitter, email_thread)
    reversed_threads = emails[::-1]
    ordered_thread = "\n\n---\n\n".join("From: " + email for email in reversed_threads)

    return ordered_thread