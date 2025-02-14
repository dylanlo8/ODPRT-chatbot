from typing import List, Tuple, Optional, Literal

from chatbot.backend.chains.email_chains import classification_chain, qa_chain
from chatbot.backend.email_processor.utils import get_all_emails
from chatbot.backend.services.logger import logger

class EmailProcessor:
    """class to process emails for optimal ingestion"""
    def __init__(
        self, 
        email_directory: str = 'docs/emails'
    ):
        self.directory = email_directory
        self.logger = logger
    
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
    
    def _filter_useful_emails(self) -> List[str]:
        """
        filter useful emails from emails

        Args:
            emails (List[str]): list of emails
            
        Returns:
            useful_emails (List[str]): list of useful emails
        """
        all_emails = get_all_emails(self.directory)
        self.logger.info(f"Total emails: {len(all_emails)}")
        useful_emails = []
        for email in all_emails:
            if self._classify_email(email) == "useful":
                useful_emails.append(email)
        self.logger.info(f"Useful emails: {len(useful_emails)}")
        return useful_emails
    
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
    
    def get_qa_pairs(self) -> Tuple[List[str], List[str]]:
        """
        get qa pairs from emails

        Returns:
            questions (List[str]): list of questions
            answers (List[str]): list of answers
        """
        useful_emails = self._filter_useful_emails()
        final_questions = []
        final_answers = []
        for email in useful_emails:
            # get list of questions and answers
            questions, answers = self._qa_email(email)
            for idx, answer in enumerate(answers):
                # filter if no answer is available
                if answer == "No answer available":
                    continue
                # append if have
                final_questions.append(questions[idx])
                final_answers.append(answers[idx])
        
        # each question and answer should be indexed together, e.g. questions[0] -> answers[0]
        return final_questions, final_answers