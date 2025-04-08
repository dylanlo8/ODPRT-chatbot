"""
This module defines a classification chain for processing email threads and attachment content.
It uses a language model to classify the relevance of the provided content.
"""

from langchain_core.prompts.chat import ChatPromptTemplate

from chatbot.backend.prompts.attachment_prompts import CLASSIFICATION_PROMPT
from chatbot.backend.schemas.structured_outputs import RelevanceClassification
from chatbot.backend.services.models.llm import gpt_4o_mini

# Define a classification chain using a chat prompt template and a language model
classification_chain = ChatPromptTemplate([
    ("system", CLASSIFICATION_PROMPT),  # System-level instructions for the model
    ("human", "{email_thread}"),  # User-provided email thread content
    ("human", "{attachment_content}")  # User-provided attachment content
]) | gpt_4o_mini.with_structured_output(RelevanceClassification)  # Use GPT model with structured output
