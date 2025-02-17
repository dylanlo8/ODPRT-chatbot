from typing import Tuple

from chatbot.backend.chains.query_chains import routing_chain, answer_chain
from chatbot.backend.services.logger import logger


class ResponseGenerator:
    """class to generate response to user queries"""

    def __init__(self):
        self.unrelated_response = "I am sorry, but I am unable to provide a response to your query at the moment."
        self.logger = logger

    def _router(
        self,
        user_query: str,
        uploaded_content: str = "",
        chat_history: str = "",
    ) -> Tuple[str, str]:
        """
        routes user queries to the appropriate response generation

        Returns:
            classification (Literal["related", "vague", "unrelated"]): classification of user query
            clarifying_question (str): clarifying question if classification is vague
        """
        result = routing_chain.invoke(
            {
                "user_query": user_query,
                "uploaded_content": uploaded_content,
                "chat_history": chat_history,
            }
        )
        classification, clarifying_question = (
            result.classification,
            result.clarifying_question,
        )
        return classification, clarifying_question

    def _generate_answer(
        self,
        user_query: str,
        uploaded_content: str = "",
        context: str = "",
        chat_history: str = "",
    ) -> str:
        """
        generates response to user queries

        Returns:
            answer: response to user query
        """
        return answer_chain.invoke(
            {
                "user_query": user_query,
                "uploaded_content": uploaded_content,
                "context": context,
                "chat_history": chat_history,
            }
        )

    def query_workflow(
        self,
        user_query: str,
        uploaded_content: str = "",
        context: str = "",
        chat_history: str = "",
    ) -> str:
        """
        complete workflow to generate response to user queries

        Returns:
            answer: response to user query
        """
        classification, clarifying_question = self._router(
            user_query=user_query,
            uploaded_content=uploaded_content,
            chat_history=chat_history,
        )

        if classification == "unrelated":
            return self.unrelated_response

        if classification == "vague":
            return clarifying_question

        return self._generate_answer(
            user_query=user_query,
            uploaded_content=uploaded_content,
            context=context,
            chat_history=chat_history,
        )
