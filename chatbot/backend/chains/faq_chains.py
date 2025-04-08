from langchain_core.prompts.chat import ChatPromptTemplate
from chatbot.backend.prompts.faq_prompts import QA_PROMPT
from chatbot.backend.schemas.structured_outputs import QAPairs
from chatbot.backend.services.models.llm import gpt_4o_mini

# Define a QA chain using a chat prompt template and a language model
qa_chain = ChatPromptTemplate([
    ("system", QA_PROMPT),  # System-level instructions for the model
    ("human", "{faq_thread}"),  # User-provided FAQ thread content
]) | gpt_4o_mini.with_structured_output(QAPairs)  # Use GPT model with structured output for QA extraction
