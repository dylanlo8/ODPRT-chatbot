import numpy as np
from typing import List, Tuple, Optional, Literal
from docx import Document

from chatbot.backend.services.logger import logger


class FAQ_Parser:
    """class to process faq document for optimal ingestion"""

    def __init__(
        self,
        faq_directory = ["docs/IEP FAQ.docx", "docs/Additional ODPRT unit FAQ.docx"],
    ):
        self.directory = faq_directory
        self.logger = logger

    def extract_qa_from_tables(self):
        """
        Extracts question-answer pairs from tables in a Word document (.docx).
        """
        qa_pairs = []
        for doc in self.directory:
            doc = Document(doc)
            for table in doc.tables:  
                for row in table.rows:
                    if len(row.cells) >= 2:  # Ensure the row has at least two columns
                        question = row.cells[0].text.strip()
                        answer = row.cells[1].text.strip()
                        
                        if question and answer:  # Avoid empty rows
                            qa_pairs.append((question, answer))
                            self.logger.info((question, answer))
        return qa_pairs
    
    def correct_qa_pairing(self, qa_pairs):
        """
        Cleans and formats extracted question-answer pairs.
        Ensures valid pairing and removes unwanted labels.
        """
        cleaned_pairs = []
        current_question = None

        for entry in qa_pairs:
            key, text = entry  # Key is "Question" or "Answer", text is the actual content

            # If the entry is a question
            if key.lower().startswith("question") or key.lower().startswith("questions"):
                if current_question:  # If there's an existing question without an answer, discard it
                    cleaned_pairs.append((current_question, "No answer provided"))
                current_question = text.strip()  # Store the new question
            
            # If the entry is an answer and there's an active question, store the pair
            elif key.lower().startswith("answer") and current_question:
                cleaned_pairs.append((current_question, text.strip()))
                current_question = None  # Reset for next pair

        return [f"question: {q}, answer: {a}" for q, a in cleaned_pairs]
    
    def extract_faq(self):
        return self.correct_qa_pairing(self.extract_qa_from_tables())