import os
from pathlib import Path
from typing import Dict, List, Optional, Union

from dotenv import load_dotenv
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import (ChatPromptTemplate,
                                    HumanMessagePromptTemplate,
                                    SystemMessagePromptTemplate)
from langchain_openai import ChatOpenAI
from langchain_mistralai import ChatMistralAI

from .prompts import OpenAIPrompts
from database_OLDGROUP.chroma_db import query_db, get_global_collection

from nemoguardrails import RailsConfig
from nemoguardrails.integrations.langchain.runnable_rails import RunnableRails

# Load .env variables
root_dir = Path(__file__).resolve().parent.parent.parent
load_dotenv(dotenv_path=root_dir / ".env")

# Remove warning when running backend
os.environ["TOKENIZERS_PARALLELISM"] = "false"

# Define types for LLM variables
chat: Union[type[ChatOpenAI], type[ChatMistralAI]]
prompts: type[OpenAIPrompts]
model_name: Optional[str]

# Get the LLM model used for the chatbot (either OpenAI or Mistral),
# and set respective variables
MODEL = os.getenv("MODEL")
if MODEL == "OPENAI":
    chat = ChatOpenAI
    prompts = OpenAIPrompts
    model_name = os.getenv("OPENAI_MODEL")
elif MODEL == "MISTRAL":
    chat = ChatMistralAI
    prompts = OpenAIPrompts
    model_name = os.getenv("MISTRAL_MODEL")


def construct_message(
    history: List[Dict[str, str]],
    prompts: List[Union[SystemMessagePromptTemplate,
                        HumanMessagePromptTemplate]]
) -> List[Union[SystemMessagePromptTemplate, HumanMessagePromptTemplate]]:
    """
    Format chat conversation history and combine it with system prompts.

    Processes the raw chat history between user and bot, properly
    formatting each message based on its source (human or system) and
    integrates them with system prompts and query prompts if present.

    Args:
        history: Chat conversation history as a list of message dictionaries
        prompts: List of system and human message templates to be included

    Returns:
        messages: List of formatted message templates, ready to be passed
        to a language model
    """
    messages = []

    # Add system prompt as first message of the list
    if isinstance(prompts[0], (str, SystemMessagePromptTemplate)):
        messages.append(prompts[0])

    # Formats history messages and appends them to list
    for past_message in history:
        content = str(past_message["text"])
        if past_message["sender"] == "user":
            messages.append(
                HumanMessagePromptTemplate.from_template(content)
            )
        else:
            messages.append(
                SystemMessagePromptTemplate.from_template(content)
            )

    # Add optional query prompt as the last message of the list
    if len(prompts) == 2 and prompts[1] is not None:
        messages.append(prompts[1])

    return messages


def get_related_documents(
        user_input: str,
        history: List[Dict[str, str]],
        model: Union[ChatOpenAI, ChatMistralAI]
) -> str:
    """
    Create a context-rich search query for querying the vector database.

    Processes the user's question along with the conversation history to
    generate an optimized search query that takes into account the full
    context of the conversation. This enhances the quality of retrieved
    documents.

    Args:
        user_input: Latest user question
        history: History of the chat conversation
        model: LLM instance to use for query generation

    Returns:
        sources: A string consisting of the retrieved documents, separated by a
        newline character
    """
    # Construct a list of prompt and conversation history
    query_messages = construct_message(history, prompts.query_prompt())
    prompt = ChatPromptTemplate.from_messages(query_messages)

    # Create and invoke the query chain
    query_chain = prompt | model | StrOutputParser()
    search_query = query_chain.invoke(user_input)

    # If most recent question is empty or if a search quert is unable to be
    # generated, return sources as empty string
    if search_query == "0":
        return ""

    # Use search query to query vector database
    related_documents = query_db(get_global_collection(), search_query, 3)
    sources = '\n'.join(related_documents["documents"][0])

    return sources


def get_completion(user_input: str, history: List[Dict[str, str]]) -> str:
    """
    Generate a safe, context-aware response to the user's query.

    Performs content safety validation on the user's input, then retrieves
    relevant documents from the vector database to generate a comprehensive
    response using the language model. The response takes into account both
    the current question and conversation history.

    Args:
        user_input: The user's current question or input
        history: Previous conversation messages as a list of dictionaries

    Returns:
        response: A string containing the language model's response to the
        user's query
    """
    # Get the path to guardrails_config and create guardrails
    current_dir = os.path.dirname(os.path.abspath(__file__))
    config_path = os.path.join(current_dir, "guardrails_config")
    config = RailsConfig.from_path(config_path)
    guardrails = RunnableRails(config)

    # If user query is blocked by the guardrails, return the result
    guardrails_result = guardrails.invoke({"input": user_input})['output']
    if guardrails_result == "I'm sorry, I can't respond to that.":
        return guardrails_result

    # Create LLM instance
    model = chat(model=model_name)

    # Get related documents from vector database
    related_documents = get_related_documents(user_input, history, model)
    if related_documents is None:
        related_documents = ""

    # Construct messages and create chain
    messages = construct_message(history, prompts.general_prompt())
    prompt = ChatPromptTemplate.from_messages(messages)
    chain = prompt | model | StrOutputParser()

    # Prepare input dictionary
    input_data = {
        'query': str(user_input),
        'sources': str(related_documents)
    }

    response = chain.invoke(input_data)
    return response


def get_email_response(history: List[Dict[str, str]]) -> str:
    """
    Generate a professional email draft to the IEP department based on
    chat history.

    Analyzes the conversation history between user and chatbot to create a
    well-structured email summarizing the user's inquiry and any unresolved
    issues that require IEP department's attention.

    Parameters:
        history: History of the chat conversation

    Returns:
        email_response: Draft of the email
    """
    # Create LLM instance
    model = chat(model=model_name)

    # Create prompt for the LLM based on the email system prompt and
    # chat history
    messages = construct_message(history, prompts.email_prompt())
    prompt = ChatPromptTemplate.from_messages(messages)

    # Create and invoke chain
    chain = prompt | model | StrOutputParser()
    email_response = chain.invoke({})

    return email_response
