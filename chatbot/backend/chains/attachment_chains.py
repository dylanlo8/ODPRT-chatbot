from langchain_core.prompts.chat import ChatPromptTemplate

from chatbot.backend.prompts.attachment_prompts import CLASSIFICATION_PROMPT
from chatbot.backend.schemas.structured_outputs import RelevanceClassification
from chatbot.backend.services.models.llm import gpt_4o_mini

classification_chain = ChatPromptTemplate([
    ("system", CLASSIFICATION_PROMPT),
    ("human", "{email_thread}"),
]) | gpt_4o_mini.with_structured_output(RelevanceClassification)