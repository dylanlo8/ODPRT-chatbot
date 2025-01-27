# flake8: noqa

import os
import pickle
from dotenv import load_dotenv
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from pathlib import Path
import json
import re

# Define the scope for Google Docs API
SCOPES = ['https://www.googleapis.com/auth/documents.readonly']

def get_google_docs_credentials():
    """
    Authenticate and obtain credentials for Google Docs API access.

    Implements OAuth 2.0 flow for authentication:
    1. Checks for existing credentials in token.pickle
    2. Refreshes expired credentials if possible
    3. Initiates new authentication flow if needed
    4. Saves valid credentials for future use

    Returns:
        google.oauth2.credentials.Credentials: Valid Google API credentials
    """
    creds = None
    # Check if token.pickle file exists for existing credentials
    if os.path.exists('chatbot/backend/database/token.pickle'):
        with open('chatbot/backend/database/token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no valid credentials, perform the authorization flow
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('chatbot/backend/database/credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for next use
        with open('chatbot/backend/database/token.pickle', 'wb') as token:
            pickle.dump(creds, token)
    return creds

# Function to extract text from Google Docs document
def extract_text_from_google_doc(doc_id):
    """
    Extract text content from a Google Docs document.

    Processes both regular paragraphs and table content, maintaining
    the document's structure while extracting all text elements.

    Args:
        doc_id (str): The Google Docs document ID to extract from

    Returns:
        str: Concatenated text content from the document
    """
    # Get credentials
    creds = get_google_docs_credentials()

    # Build the Google Docs service
    service = build('docs', 'v1', credentials=creds)

    # Get the document content
    doc = service.documents().get(documentId=doc_id).execute()

    # Initialize a list to hold extracted text
    extracted_text = []

    # Iterate through the document content
    for element in doc.get('body', {}).get('content', []):
        if 'paragraph' in element:
            # Extract text from regular paragraphs
            for paragraph in element['paragraph']['elements']:
                if 'textRun' in paragraph:
                    text_content = paragraph['textRun']['content']
                    extracted_text.append(text_content)
        elif 'table' in element:
            # Extract text from table cells
            for row in element['table']['tableRows']:
                for cell in row['tableCells']:
                    for cell_content in cell.get('content', []):
                        if 'paragraph' in cell_content:
                            for paragraph in cell_content['paragraph']['elements']:
                                if 'textRun' in paragraph:
                                    text_content = paragraph['textRun']['content']
                                    extracted_text.append(text_content)

    return ''.join(extracted_text)

def chunk_data(extracted_text, data_type):
    """
    Process and structure extracted text into FAQ or email format.

    Splits and organizes raw text into structured JSON format based on
    predefined patterns and categories.

    Args:
        extracted_text (str): Raw text extracted from Google Doc
        data_type (str): Type of data to process ('faq' or 'email')

    Creates two JSON files:
        1. Raw text file: Stores the initial extracted text
        2. Processed data file: Stores the structured Q&A pairs
    """
    # Determine file paths based on data type
    input_file = f"chatbot/backend/database/data/{'FAQ_text' if data_type == 'faq' else 'email_text'}.json"
    output_file = f"chatbot/backend/database/data/{'FAQ_data' if data_type == 'faq' else 'email_data'}.json"

    # Write extracted text to initial json file
    with open(input_file, "w") as f:
        json.dump([extracted_text], f)

    # Read the json file
    with open(input_file, "r") as file:
        data = json.load(file)

    # Define common categories/subjects
    categories = [
        "Agreement Type Enquiries",
        "General Enquiries",
        "IEP Contracting Hub Enquiries",
        "Redirect - Technology Transfer & Innovation (TTI) Enquiries",
        "Redirect – Office of Legal Affairs (OLA) Enquiries",
        "Redirect to IRB Enquiries"
    ]

    # Define patterns based on data type
    if data_type == "faq":
        pattern_list = ["Question", "Answer"] + categories
    else:
        pattern_list = ["Q&A pair", "Subject"] + categories

    # Split the data
    pattern = r'(' + '|'.join(re.escape(p) for p in pattern_list) + r')'
    split_data = re.split(pattern, data[0])

    # Clean and process the data
    output_data = []
    current_category = ""
    current_subject = ""
    id_counter = 1

    if data_type == "faq":
        # Process FAQ data
        is_question = False
        is_answer = False
        current_question = ""

        for item in split_data:
            item = item.replace('\n', '')
            if not item or item.isspace():
                continue

            if item in categories:
                current_category = item
            elif item == "Question":
                is_question = True
                is_answer = False
            elif item == "Answer":
                is_answer = True
                is_question = False
            else:
                if is_question:
                    current_question = item
                if is_answer:
                    doc = {
                        "QA_pair": f"Question: \n{current_question}\nAnswer: \n{item}",
                        "Subject": current_category,
                        "id": f"FAQ_{id_counter}"
                    }
                    output_data.append(doc)
                    id_counter += 1
    else:
        # Process email data
        is_subject = False
        is_qa_pair = False

        for item in split_data:
            item = item.replace('\n', '')
            if not item or item.isspace():
                continue

            if item in categories:
                current_category = item
            elif item == "Subject":
                is_subject = True
                is_qa_pair = False
            elif item == "Q&A pair":
                is_qa_pair = True
                is_subject = False
            else:
                if is_subject:
                    current_subject = item
                if is_qa_pair and item != "Q&A pair":
                    doc = {
                        "QA_pair": item,
                        "Subject": current_subject,
                        "id": f"Email_{id_counter}",
                        "Category": current_category
                    }
                    output_data.append(doc)
                    id_counter += 1

    # Write the processed data to output file
    with open(output_file, "w") as f:
        json.dump(output_data, f)

def get_clean_data(doc_id, data_type):
    """
    Main function to extract and process Google Docs data.

    Coordinates the extraction and processing of document content.

    Args:
        doc_id (str): Google Docs document ID to process
        data_type (str): Type of data to process ('faq' or 'email')
    """
    # Extract raw text from Google Doc
    extracted_text = extract_text_from_google_doc(doc_id)
    # Process and structure the extracted text
    chunk_data(extracted_text, data_type)
