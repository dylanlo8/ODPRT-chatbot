from chatbot.backend.services.models.embedding_model import embedding_model
from chatbot.backend.services.logger import logger
from chatbot.backend.services.models.models import vlm
from typing import Literal
from langchain_experimental.text_splitter import SemanticChunker
import os
import mimetypes
import docx
from PIL import Image
import numpy as np
import pdfplumber
from docx import Document
import io
import cv2
from pdf2image import convert_from_path
from typing import List, Tuple, Optional, Literal
import requests
import json
from docx2pdf import convert
import shutil
from fpdf import FPDF


class DocumentParser:
    """class to parse attachments and return ingestable chunks of information"""

    def __init__(
        self,
        attachment_directory: str = "processed_docs/emails_with_attachments",
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
    
    def filter_useful_attachments(self) -> List[str]:
        """
        Filters and processes useful attachments from emails in 'processed_docs/emails_with_attachments'.

        Returns:
            List[str]: List of relevant processed attachment file paths.
        """
        useful_attachments = []
        
        if not os.path.exists(self.directory):
            self.logger.warning(f"Directory {self.directory} does not exist.")
            return []

        for email_folder in os.listdir(self.directory):
            email_path = os.path.join(self.directory, email_folder)
            original_attachments_path = os.path.join(email_path, "original_attachments")
            processed_attachments_path = os.path.join(email_path, "processed_attachments")
            cleaned_email_path = os.path.join(email_path, "cleaned_msg.txt")

            if not os.path.isdir(email_path):
                continue

            if not os.path.exists(cleaned_email_path):
                self.logger.warning(f"Missing cleaned email: {cleaned_email_path}")
                continue
            
            with open(cleaned_email_path, "r", encoding="utf-8") as f:
                email_thread = f.read().strip()

            os.makedirs(processed_attachments_path, exist_ok=True)

            for file in os.listdir(original_attachments_path):
                attachment_path = os.path.join(original_attachments_path, file)
                file_ext = file.lower().split(".")[-1]

                if file == "cleaned_msg.txt":
                    continue

                processed_file_path = ""

                if file_ext in ["png", "jpg", "jpeg", "bmp", "tiff"]:
                    payload = vlm._build_payloads_for_attachments(email_thread, [attachment_path])[0]
                    response = requests.post(vlm.api, headers=vlm.headers, json=payload)

                    try:
                        response_json = response.json()
                        answer = response_json.get("choices", [{}])[0].get("message", {}).get("content", "")

                        if answer.strip().lower() == "relevant":
                            processed_file_path = os.path.join(processed_attachments_path, file)
                            shutil.copy(attachment_path, processed_file_path)

                    except json.JSONDecodeError:
                        self.logger.error(f"Invalid JSON response for {attachment_path}: {response.text}")

                elif file_ext == "docx":
                    # Convert DOCX to PDF first
                    pdf_path = self.convert_docx_to_pdf(attachment_path)
                    relevant_images = self.classify_attachment_relevance(email_thread, pdf_path)

                    # Save only relevant pages
                    if relevant_images:
                        processed_file_path = os.path.join(processed_attachments_path, os.path.basename(pdf_path))
                        shutil.copy(relevant_images, processed_file_path)

                elif file_ext == "pdf":
                    # Classify pages directly from the PDF
                    relevant_images = self.classify_attachment_relevance(email_thread, attachment_path)

                    # Save only relevant pages
                    if relevant_images:
                        processed_file_path = os.path.join(processed_attachments_path, os.path.basename(attachment_path))
                        shutil.copy(relevant_images, processed_file_path)

                # If a processed file was created, add it to the list of useful attachments
                if processed_file_path:
                    useful_attachments.append(processed_file_path)

            # Cleanup intermediate processing files (like extracted images)
            temp_image_dirs = [os.path.join(email_path, "temp_images")]
            for temp_dir in temp_image_dirs:
                shutil.rmtree(temp_dir, ignore_errors=True)

        self.logger.info(f"Total useful attachments: {len(useful_attachments)}")
        return useful_attachments

    
    def convert_docx_to_pdf(self, docx_path: str) -> str:
        """
        Converts a DOCX file to PDF.

        Args:
            docx_path (str): Path to the DOCX file.

        Returns:
            str: Path to the generated PDF file.
        """
        output_pdf_path = os.path.join(os.path.dirname(docx_path), "converted.pdf")
        convert(docx_path, output_pdf_path)
        return output_pdf_path
    
    def convert_pdf_to_images(self, pdf_path: str, output_folder: str = None, dpi: int = 300) -> List[str]:
        """
        Converts a PDF into images, one image per page.

        Args:
            pdf_path (str): Path to the PDF file.
            output_folder (str, optional): Folder to save extracted images.
            dpi (int, optional): Resolution of the output images.

        Returns:
            List[str]: List of paths to the saved image files.
        """
        if output_folder is None:
            output_folder = os.path.join(os.path.dirname(pdf_path), "temp_images")
        os.makedirs(output_folder, exist_ok=True)

        images = convert_from_path(pdf_path, dpi=dpi)
        image_paths = []

        for i, image in enumerate(images):
            image_path = os.path.join(output_folder, f"page_{i+1}.png")
            image.save(image_path, "PNG")
            image_paths.append(image_path)

        return image_paths

    def classify_attachment_relevance(self, email_thread: str, attachment_path: str) -> str:
        """
        Classifies whether an attachment (PDF, DOCX, or images) is relevant based on the email context.

        Args:
            email_thread (str): The cleaned email text.
            attachment_path (str): The file path to the attachment.

        Returns:
            str: Path to the processed relevant PDF, or "not_relevant" if no relevant content is found.
        """
        file_ext = attachment_path.lower().split(".")[-1]  # Extract file extension
        useful_images = []

        # Convert attachment into images (for classification)
        if file_ext in ["pdf"]:
            images = self.convert_pdf_to_images(attachment_path)  # Convert PDF to images
        elif file_ext in ["docx"]:
            pdf_path = self.convert_docx_to_pdf(attachment_path)  # Convert DOCX → PDF
            images = self.convert_pdf_to_images(pdf_path)  # Convert PDF → Images
        elif file_ext in ["png", "jpg", "jpeg", "bmp", "tiff"]:
            images = [attachment_path]  # It's already an image
        else:
            self.logger.warning(f"Unsupported file format: {attachment_path}")
            return "not_relevant"

        # Build payloads for each extracted page/image
        payloads = vlm._build_payloads_for_attachments(email_thread, images)

        for image_path, payload in zip(images, payloads):
            response = requests.post(vlm.api, headers=vlm.headers, json=payload)

            try:
                response_json = response.json()
                answer = response_json.get("choices", [{}])[0].get("message", {}).get("content", "")

                if not answer.strip():
                    self.logger.error(f"Empty response for {image_path}. Skipping.")
                    continue 

                self.logger.info(f"Raw model response for {image_path}: {answer}")

                # Parse JSON response
                try:
                    json_answer = json.loads(answer)
                    classification = json_answer.get("classification", "not_relevant")
                    justification = json_answer.get("justification", "")

                    self.logger.info(f"Classification: {classification}, Justification: {justification}")

                    if classification == "relevant":
                        useful_images.append(image_path)
                        self.logger.info(f"✔ Relevant Page: {image_path}")

                except json.JSONDecodeError:
                    self.logger.error(f"Invalid JSON format in response: {answer}")

            except requests.exceptions.RequestException as e:
                self.logger.error(f"VLM API request failed: {e}")

        # If relevant pages exist, save them as a new processed PDF
        if useful_images:
            processed_pdf_path = self.combine_images_into_pdf(useful_images, attachment_path)
            self.logger.info(f"Processed PDF saved at: {processed_pdf_path}")
            return processed_pdf_path

        self.logger.info(f"No relevant content found in {attachment_path}")
        return "not_relevant"


            
    def combine_images_into_pdf(self, useful_images: List[str], attachment_path: str) -> str:
        """
        Combines relevant pages (images) into a single PDF.

        Args:
            useful_images (List[str]): List of image paths for relevant pages.
            attachment_path (str): The original attachment file path.

        Returns:
            str: Path to the final processed PDF.
        """
        if not useful_images:
            self.logger.info(f"No relevant pages found for {attachment_path}. Skipping PDF creation.")
            return ""

        processed_folder = os.path.join(os.path.dirname(os.path.dirname(attachment_path)), "processed_attachments")
        os.makedirs(processed_folder, exist_ok=True)
        output_pdf_path = os.path.join(processed_folder, os.path.basename(attachment_path).replace(".pdf", "_processed.pdf"))

        pdf = FPDF()
        for image_path in useful_images:
            pdf.add_page()
            pdf.image(image_path, x=0, y=0, w=210, h=297)

        pdf.output(output_pdf_path, "F")
        self.logger.info(f"Saved processed PDF: {output_pdf_path}")

        temp_image_dir = os.path.dirname(useful_images[0])
        shutil.rmtree(temp_image_dir, ignore_errors=True)

        return output_pdf_path

    def extract_images_from_docx(docx_path: str, output_folder: str = None) -> List[str]:
        """
        Extracts images from a DOCX file and saves them as image files.

        Args:
            docx_path (str): Path to the DOCX file.
            output_folder (str, optional): Folder to save extracted images.

        Returns:
            List[str]: List of paths to the saved image files.
        """
        doc = docx.Document(docx_path)

        if output_folder is None:
            output_folder = os.path.splitext(docx_path)[0] + "_images"
        os.makedirs(output_folder, exist_ok=True)

        image_paths = []
        image_count = 0

        for rel in doc.part.rels:
            if "image" in doc.part.rels[rel].target_ref:
                image_data = doc.part.rels[rel].target_part.blob

                image = Image.open(io.BytesIO(image_data))
                image_filename = f"docx_image_{image_count+1}.png"
                image_path = os.path.join(output_folder, image_filename)
                image.save(image_path, "PNG")
                
                image_paths.append(image_path)
                image_count += 1

        return image_paths
    

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
        save_directory = os.path.join(os.getcwd(), "extracted_images", )
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

        save_directory = os.path.join(os.getcwd(), "processed_docs/attachment_chunks/email")
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
        return text, images
    
    def chunk_text(self, text):
        os.environ["TOKENIZERS_PARALLELISM"] = "false"
        semantic_chunker = SemanticChunker(
            embedding_model,
            breakpoint_threshold_type="percentile"
        )
        semantic_chunks = semantic_chunker.create_documents([text])

        return [chunk.page_content for chunk in semantic_chunks]