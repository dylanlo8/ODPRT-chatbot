from typing import List, Tuple, Optional, Literal

from chatbot.backend.chains.email_chains import classification_chain, qa_chain
from chatbot.backend.email_processor.utils import read_email, clean_email

class EmailProcessor:
    """class to process emails for optimal ingestion"""
    def __init__(self, directory: str):
        self.directory = directory
    
    def _classify_email(
        self,
        email_thread: str
    ) -> Literal["useful", "not_useful"]:
        """
        classify email thread based on usefulness

        Args:
            email_thread (str): email thread
            
        Returns:
            classification (Literal["useful", "not_useful"]): classification of email thread
        """
        # invoke chain
        response = classification_chain.invoke({"email_thread": email_thread})
        return response.classification
    
    def _qa_email(
        self,
        email_thread: str
    ) -> Tuple[List[str], List[str]]:
        """
        qa email thread

        Args:
            email_thread (str): email thread
            
        Returns:
            questions (List[str]): list of questions
            answers (List[str]): list of answers
        """
        # invoke chain
        response = qa_chain.invoke({"email_thread": email_thread})
        return response.questions, response.answers