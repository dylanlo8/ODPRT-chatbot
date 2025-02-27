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
        faq_directory = ["docs/IEP FAQ.docx", "docs/Additional ODPRT unit FAQ.docx"],
        similarity_threshold: float = 0.85,
    ):
        self.directory = faq_directory
        self.similarity_threshold = similarity_threshold
        self.embedding_model = embedding_model
        self.logger = logger

    def extract_faq(self):
        """Extracts text from a Word document."""
        full_text = []
        for doc in self.directory:
            doc = Document(doc)

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

        return self._merge_qa_pairs(
            questions=final_questions, answers=final_answers
        )