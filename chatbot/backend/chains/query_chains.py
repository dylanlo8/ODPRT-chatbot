"""
This module defines chains for processing user queries.
It includes chains for classifying queries, generating responses, and creating email templates.
"""

from langchain_core.prompts.chat import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

from chatbot.backend.prompts.query_prompts import (
    ANSWER_PROMPT,
    ROUTING_PROMPT,
    EMAIL_TEMPLATE,
)
from chatbot.backend.schemas.structured_outputs import SemanticRouting, EmailTemplate
from chatbot.backend.services.models.llm import gpt_4o_mini

# Define a chain for classifying user queries
routing_chain = ChatPromptTemplate.from_messages(
    [
        ("system", ROUTING_PROMPT),
        ("human", "{user_query}"),
        ("human", "{uploaded_content}"),
        ("human", "{chat_history}"),
    ]
) | gpt_4o_mini.with_structured_output(SemanticRouting)

# Define a chain for generating responses to user queries
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

# Define a chain for generating email templates based on chat history
generate_email_chain = ChatPromptTemplate.from_messages(
    [
        ("system", EMAIL_TEMPLATE),
        ("human", "{chat_history}"),
    ]
) | gpt_4o_mini.with_structured_output(EmailTemplate)
