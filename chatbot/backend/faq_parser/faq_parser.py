import numpy as np

from sklearn.metrics.pairwise import cosine_similarity
from typing import List, Tuple, Optional, Literal
from docx import Document

from chatbot.backend.chains.faq_chains import qa_chain
from chatbot.backend.services.models.embedding_model import embedding_model
from chatbot.backend.services.logger import logger


class FAQ_Parser:
    """class to process faq document for optimal ingestion"""

    def __init__(
        self,
        faq_directory: str = "docs/IEP FAQ.docx",
        similarity_threshold: float = 0.85,
    ):
        self.directory = faq_directory
        self.similarity_threshold = similarity_threshold
        self.embedding_model = embedding_model
        self.logger = logger

    def extract_faq(self):
        """Extracts text from a Word document."""
        doc = Document(self.directory)
        full_text = []

        for para in doc.paragraphs:
            full_text.append(para.text)

        for table in doc.tables:
            for row in table.rows:
                row_text = [cell.text.strip() for cell in row.cells]
                full_text.append("\t".join(row_text))

        return '\n'.join(full_text)

    def _qa_faq(
        self,
        faq_thread: str,
    ) -> Tuple[List[str], List[str]]:
        # invoke chain
        response = qa_chain.invoke({"faq_thread": faq_thread})
        return response.questions, response.answers

    def _merge_qa_pairs(
        self,
        questions: List[str],
        answers: List[str],
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
        texts: List[str],
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
        qa_pairs: List[str],
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
        final_questions = []
        final_answers = []
        questions, answers = self._qa_faq(self.extract_faq())
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