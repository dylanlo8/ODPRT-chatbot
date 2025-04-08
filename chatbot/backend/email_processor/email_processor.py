import numpy as np

from sklearn.metrics.pairwise import cosine_similarity
from typing import List, Tuple, Optional, Literal

from chatbot.backend.chains.email_chains import classification_chain, qa_chain
from chatbot.backend.email_processor.utils import get_all_emails_and_attachments
from chatbot.backend.services.models.embedding_model import embedding_model
from chatbot.backend.services.logger import logger
import os
import shutil


"""
This module defines the EmailProcessor class, which processes emails for ingestion.
It includes methods for filtering useful emails, extracting QA pairs, and deduplicating content.
"""

class EmailProcessor:
    """
    A class to process emails for optimal ingestion.

    Attributes:
        directory (str): Directory containing email data.
        similarity_threshold (float): Threshold for determining semantic similarity.
        embedding_model: Model used for computing embeddings.
        logger: Logger instance for logging messages.
    """

    def __init__(
        self,
        email_directory: str = "docs/emails",
        similarity_threshold: float = 0.85,
    ):
        self.directory = email_directory
        self.similarity_threshold = similarity_threshold
        self.embedding_model = embedding_model
        self.logger = logger

    def _classify_email(self, email_thread: str) -> Literal["useful", "not_useful"]:
        """
        Classifies an email thread based on its usefulness.

        Args:
            email_thread (str): The email thread content.

        Returns:
            Literal["useful", "not_useful"]: Classification of the email thread.
        """

        # invoke chain
        response = classification_chain.invoke({"email_thread": email_thread})
        return response.classification

    def _filter_useful_emails(self) -> List[str]:
        """
        Filters useful emails from the extracted email directory.
        Deletes entire email directories (including attachments) if emails are not useful.

        Returns:
            List[str]: Paths of useful emails.
        """
        cleaned_email_paths, email_attachments = get_all_emails_and_attachments()
        self.logger.info(f"Total emails: {len(cleaned_email_paths)}")

        useful_emails = []

        for email_path in cleaned_email_paths:
            cleaned_email_txt = os.path.join(email_path)
            email_dir = os.path.dirname(email_path)

            if not os.path.exists(cleaned_email_txt):
                self.logger.warning(f"Missing cleaned email file: {cleaned_email_txt}. Deleting directory.")
                shutil.rmtree(email_dir, ignore_errors=True)
                continue
            
            try:
                with open(cleaned_email_txt, "r", encoding="utf-8") as f:
                    email_content = f.read().strip()
            except Exception as e:
                self.logger.error(f"Error reading {cleaned_email_txt}: {e}. Deleting directory.")
                shutil.rmtree(email_dir, ignore_errors=True)
                continue

            if self._classify_email(email_content) == "useful":
                useful_emails.append(email_content)
            else:
                self.logger.info(f"Email deemed not useful. Deleting directory: {email_dir}")
                shutil.rmtree(email_dir, ignore_errors=True)

        self.logger.info(f"Useful emails: {len(useful_emails)}")
        return useful_emails

    def _qa_email(self, email_thread: str) -> Tuple[List[str], List[str]]:
        """
        Extracts questions and answers from an email thread.

        Args:
            email_thread (str): The email thread content.

        Returns:
            Tuple[List[str], List[str]]: A tuple containing lists of questions and answers.
        """
        # invoke chain
        response = qa_chain.invoke({"email_thread": email_thread})
        return response.questions, response.answers

    def _merge_qa_pairs(self, questions: List[str], answers: List[str]) -> List[str]:
        """
        Merges questions and answers into QA pairs.

        Args:
            questions (List[str]): List of questions.
            answers (List[str]): List of answers.

        Returns:
            List[str]: List of merged QA pairs.
        """
        qa_pairs = []
        for idx, question in enumerate(questions):
            answer = answers[idx]
            qa = f"question: {question} answer: {answer}"
            qa_pairs.append(qa)
        return qa_pairs

    def _find_duplicates(self, texts: List[str]) -> List[int]:
        """
        Finds duplicate texts based on semantic similarity.

        Args:
            texts (List[str]): List of text strings to check for duplicates.

        Returns:
            List[int]: Indices of texts that are duplicates.
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

    def _dedup_qa_pairs(self, qa_pairs: List[str]) -> List[str]:
        """
        Removes duplicate QA pairs based on semantic similarity.

        Args:
            qa_pairs (List[str]): List of question-answer pairs.

        Returns:
            List[str]: Deduplicated question-answer pairs.
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
        Extracts QA pairs from emails.

        Returns:
            List[str]: List of deduplicated QA pairs.
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
            questions=final_questions, answers=final_answers
        )
        # dedup similar QA pairs to retain highest quality data
        return self._dedup_qa_pairs(qa_pairs=qa_pairs)
