from langchain_core.prompts.chat import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

from chatbot.backend.prompts.query_prompts import ANSWER_PROMPT, ROUTING_PROMPT
from chatbot.backend.schemas.structured_outputs import SemanticRouting
from chatbot.backend.services.models.llm import gpt_4o_mini

# classifies user queries
routing_chain = ChatPromptTemplate.from_messages(
    [
        ("system", ROUTING_PROMPT),
        ("human", "{user_query}"),
        ("human", "{uploaded_content}"),
        ("human", "{chat_history}"),
    ]
) | gpt_4o_mini.with_structured_output(SemanticRouting)

# generates responses
answer_chain = (
    ChatPromptTemplate.from_messages(
        [
            ("system", ANSWER_PROMPT),
            ("human", "{user_query}"),
            ("human", "{uploaded_content}"),
            ("human", "{context}"),
            ("human", "{chat_history}"),
        ]
    )
    | gpt_4o_mini
    | StrOutputParser()
)
