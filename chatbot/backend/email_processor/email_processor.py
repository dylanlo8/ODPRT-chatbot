import numpy as np

from sklearn.metrics.pairwise import cosine_similarity
from typing import List, Tuple, Optional, Literal

from chatbot.backend.chains.email_chains import classification_chain, qa_chain
from chatbot.backend.email_processor.utils import get_all_emails
from chatbot.backend.services.models.embedding_model import embedding_model
from chatbot.backend.services.logger import logger

class EmailProcessor:
    """class to process emails for optimal ingestion"""
    def __init__(
        self, 
        email_directory: str = 'docs/emails',
        similarity_threshold: float = 0.85
    ):
        self.directory = email_directory
        self.similarity_threshold = similarity_threshold
        self.embedding_model = embedding_model
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
    
    def _merge_qa_pairs(
        self,
        questions: List[str],
        answers: List[str]
    ) -> List[str]:
        """
        merge questions and answers

        Args:
            questions (List[str]): list of questions
            answers (List[str]): list of answers
            
        Returns:
            qa_pairs (List[str]): list of questions and answers
        """
        qa_pairs = []
        for idx, question in enumerate(questions):
            answer = answers[idx]
            qa = f"question: {question} answer: {answer}"
            qa_pairs.append(qa)
        return qa_pairs
    
    def _find_duplicates(
        self, 
        texts: List[str]
    ) -> List[int]:
        """
        find duplicate texts based on semantic similarity
        
        Args:
            texts (List[str]): List of text strings to check for duplicates
            
        Returns:
            List[int]: Indices of texts that are duplicates
        """
        # compute embeddings for all texts
        embeddings = self.embedding_model.compute_embeddings(texts)

        # compute pairwise similarities using cosine similarity
        similarities = cosine_similarity(embeddings)
        
        # find indices of similar pairs
        duplicate_indices = set()
        for i in range(len(texts)):
            for j in range(i + 1, len(texts)):
                if similarities[i][j] > self.similarity_threshold:
                    # keep the first occurrence, mark the later one as duplicate
                    duplicate_indices.add(j)
        
        return sorted(list(duplicate_indices))
    
    def _dedup_qa_pairs(
        self, 
        qa_pairs: List[str]
    ) -> List[str]:
        """
        remove duplicate QA pairs based on semantic similarity.
        
        Args:
            qa_pairs (List[str]): List of question-answer pairs
            
        Returns:
            List[str]: Deduplicated question-answer pairs
        """
        if not qa_pairs:
            return []
        
        # find duplicates based on combined question-answer similarity
        duplicate_indices = self._find_duplicates(qa_pairs)
        
        # create deduplicated list preserving original format
        unique_pairs = []
        for idx, qa in enumerate(qa_pairs):
            if idx not in duplicate_indices:
                unique_pairs.append(qa)
                
        self.logger.info(f"Removed {len(duplicate_indices)} duplicate QA pairs")
        return unique_pairs
    
    def get_qa_pairs(self) -> List[str]:
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

        qa_pairs = self._merge_qa_pairs(
            questions=final_questions,
            answers=final_answers
        )
        # dedup similar QA pairs to retain highest quality data
        return self._dedup_qa_pairs(qa_pairs=qa_pairs)