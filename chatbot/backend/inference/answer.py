from chatbot.backend.chains.query_chains import routing_chain, answer_chain


def semantic_router(
    user_query: str,
    chat_history: str,
) -> str:
    """
    routes user queries to the appropriate response generation

    Args:
        user_query (str): user query
        chat_history (str): chat history

    Returns:
        answer (str): response to user query
    """
    result = routing_chain.invoke(
        {
            "user_query": user_query,
            "chat_history": chat_history,
        }
    )
    classification = result.classification

    if classification == "related":
        return generate_answer(user_query)

    if classification == "vague":
        return result.clarifying_question

    return "The query is unrelated to IEP's responsibilities; I am unable to provide an answer."


def generate_answer(
    user_query: str,
    context: str,
    chat_history: str,
) -> str:
    """
    generates response to user queries

    Args:
        user_query (str): query
        context (str): retrieved context from vector db
        chat_history (str): chat history

    Returns:
        answer: response to user query
    """
    return answer_chain.invoke(
        {
            "user_query": user_query,
            "chat_history": chat_history,
            "context": context,
        }
    )
