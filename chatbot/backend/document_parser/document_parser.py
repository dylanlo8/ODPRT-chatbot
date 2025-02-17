from chatbot.backend.services.models.embedding_model import embedding_model
from chatbot.backend.services.logger import logger
from chatbot.backend.chains.attachment_chains import classification_chain
from typing import List, Tuple, Optional, Literal

import os
import mimetypes
import fitz
import docx
import pytesseract
from PIL import Image
import numpy as np
import logging
from sklearn.cluster import KMeans
import pdfplumber
from docx import Document
import io
import os
import cv2
import numpy as np
from pdf2image import convert_from_path
import fitz  # PyMuPDF
from PIL import Image


class DocumentParser:
    """class to parse attachments and return ingestable chunks of information"""

    def __init__(
        self,
        attachment_directory: str = "docs/attachments",
        similarity_threshold: float = 0.85,
    ):
        self.directory = attachment_directory
        self.similarity_threshold = similarity_threshold
        self.embedding_model = embedding_model
        self.logger = logger

    def read_attachments(self):
        """Reads all attachments in the directory and returns a list of file paths."""
        files = []
        for root, _, filenames in os.walk(self.directory):
            for filename in filenames:
                files.append(os.path.join(root, filename))
        return files
    
    def classify_attachment_relevance(
            self,
            email_thread: str,
        ) -> Literal["relevant", "not_relevant"]:
            """
            classify email thread based on usefulness

            Args:
                email_thread (str): email thread

            Returns:
                classification (Literal["useful", "not_useful"]): classification of email thread
            """
            response = classification_chain.invoke({"email_thread": email_thread})
            return response.classification
    
    def extract_text_from_pdf(self, file_path: str):
        """Extracts text from a PDF file."""
        extracted_text = ""
        with pdfplumber.open(file_path) as pdf:
            for i, page in enumerate(pdf.pages):
                text = page.extract_text()
                if text:
                    extracted_text += f"\nPage {i+1}\n{text.strip()}\n\n"
        return extracted_text
    
    def extract_images_from_pdf(self, file_path: str, min_contour_area=5000):
        """Extracts images from a PDF file."""
        save_directory = os.path.join(os.getcwd(), "extracted_data/extracted_images")
        os.makedirs(save_directory, exist_ok=True)

        poppler_path = "/opt/homebrew/bin"  # Adjust this if needed
        images = convert_from_path(file_path,  poppler_path = poppler_path)
        extracted_figures = {}

        for page_num, image in enumerate(images):
            open_cv_image = np.array(image)
            open_cv_image = cv2.cvtColor(open_cv_image, cv2.COLOR_RGB2BGR)

            gray = cv2.cvtColor(open_cv_image, cv2.COLOR_BGR2GRAY)
            edges = cv2.Canny(gray, 50, 150)

            contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

            figure_paths = []
            figure_count = 0

            for contour in contours:
                if cv2.contourArea(contour) < min_contour_area:
                    continue

                x, y, w, h = cv2.boundingRect(contour)
                figure_image = image.crop((x, y, x + w, y + h))

                figure_path = os.path.join(save_directory, f"page_{page_num+1}_figure_{figure_count+1}.png")
                figure_image.save(figure_path, "PNG")
                figure_paths.append(figure_path)

                figure_count += 1

            extracted_figures[f"Page {page_num+1}"] = figure_paths

        return extracted_figures

    def extract_text_from_docx(self, file_path: str):
        """Extracts text from a Word document."""
        doc = Document(file_path)
        full_text = []

        for para in doc.paragraphs:
            full_text.append(para.text)

        for table in doc.tables:
            for row in table.rows:
                row_text = [cell.text.strip() for cell in row.cells]
                full_text.append("\t".join(row_text))

        return '\n'.join(full_text)
    
    def extract_images_from_docx(self, file_path: str):
        """Extracts images from a Word document and saves them to a directory."""

        save_directory = os.path.join(os.getcwd(), "extracted_data/extracted_images")
        os.makedirs(save_directory, exist_ok=True)

        doc = docx.Document(file_path)
        extracted_images = {}

        image_count = 0

        for rel in doc.part.rels:
            if "image" in doc.part.rels[rel].target_ref:
                image_count += 1
                image_data = doc.part.rels[rel].target_part.blob

                image = Image.open(io.BytesIO(image_data))

                image_filename = f"docx_image_{image_count}.png"
                image_path = os.path.join(save_directory, image_filename)
                image.save(image_path, "PNG")

                extracted_images[f"Image {image_count}"] = image_path

                print(f"Saved: {image_path}")

        return extracted_images
    
    def separate_text_and_images(self, file_path: str):
        """
        Extracts both text and images from an attachment.
        Returns a tuple: (extracted_text, list_of_images).
        """
        mime_type, _ = mimetypes.guess_type(file_path)
        text = ""
        images = []

        if mime_type and "pdf" in mime_type:
            text = self.extract_text_from_pdf(file_path)
            images = self.extract_images_from_pdf(file_path)
        elif mime_type and "word" in mime_type or file_path.endswith(".docx"):
            text = self.extract_text_from_docx(file_path)
            images = self.extract_images_from_docx(file_path)
        elif mime_type and "image" in mime_type:
            images.append(file_path)
            text = self.extract_text_from_image(file_path)
        return text, images

docParser = DocumentParser()
text, images = docParser.separate_text_and_images("/Users/lishuyao/Documents/NUS/MODS/Y3S2/Capstone/ODPRT-chatbot/docs/IEP FAQ.docx")
print(text)
# texts, images = docParser.separate_text_and_images("/Users/lishuyao/Documents/NUS/MODS/Y3S2/Capstone/ODPRT-chatbot/docs/sample_docx.docx")
# print(texts)