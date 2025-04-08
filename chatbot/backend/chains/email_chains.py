from langchain_core.prompts.chat import ChatPromptTemplate
from chatbot.backend.prompts.email_prompts import CLASSIFICATION_PROMPT, QA_PROMPT
from chatbot.backend.schemas.structured_outputs import UsefulnessClassification, QAPairs
from chatbot.backend.services.models.llm import gpt_4o_mini

# Define a classification chain using a chat prompt template and a language model
classification_chain = ChatPromptTemplate([
    ("system", CLASSIFICATION_PROMPT),  # System-level instructions for the model
    ("human", "{email_thread}"),  # User-provided email thread content
]) | gpt_4o_mini.with_structured_output(UsefulnessClassification)  # Use GPT model with structured output for classification

# Define a QA chain using a chat prompt template and a language model
qa_chain = ChatPromptTemplate([
    ("system", QA_PROMPT),  # System-level instructions for the model
    ("human", "{email_thread}"),  # User-provided email thread content
]) | gpt_4o_mini.with_structured_output(QAPairs)  # Use GPT model with structured output for QA extraction
