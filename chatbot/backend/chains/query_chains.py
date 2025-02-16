from langchain_core.prompts.chat import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

from chatbot.backend.prompts.query_prompts import ANSWER_PROMPT, ROUTING_PROMPT
from chatbot.backend.schemas.structured_outputs import SemanticRouting
from chatbot.backend.services.models.llm import gpt_4o_mini

answer_chain = ChatPromptTemplate([
    ("system", ANSWER_PROMPT),
    ("human", "{user_query}"),
]) | gpt_4o_mini | StrOutputParser()

routing_chain = ChatPromptTemplate([
    ("system", ROUTING_PROMPT),
    ("human", "{user_query}"),
]) | gpt_4o_mini.with_structured_output(SemanticRouting)