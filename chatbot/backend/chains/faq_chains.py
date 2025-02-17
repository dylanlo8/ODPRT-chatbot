from langchain_core.prompts.chat import ChatPromptTemplate

from chatbot.backend.prompts.faq_prompts import QA_PROMPT
from chatbot.backend.schemas.structured_outputs import QAPairs
from chatbot.backend.services.models.llm import gpt_4o_mini

qa_chain = ChatPromptTemplate([
    ("system", QA_PROMPT),
    ("human", "{faq_thread}"),
]) | gpt_4o_mini.with_structured_output(QAPairs)
