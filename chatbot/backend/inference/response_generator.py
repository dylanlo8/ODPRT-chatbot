from typing import List, Tuple

from chatbot.backend.chains.query_chains import (
    routing_chain,
    answer_chain,
    generate_email_chain,
)
from chatbot.backend.services.logger import logger
from chatbot.backend.services.vector_db.db import vector_db


class ResponseGenerator:
    """class to generate response to user queries"""

    def __init__(self):
        self.unrelated_response = "I am sorry, but I am unable to provide a response to your query at the moment."
        self.vector_db = vector_db
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

        classification, reasoning, clarifying_question = (
            result.classification,
            result.reasoning,
            result.clarifying_question,
        )

        return classification, reasoning, clarifying_question

    def _generate_answer(
        self,
        user_query: str,
        uploaded_content: str = "",
        chat_history: str = "",
    ) -> str:
        """
        generates response to user queries

        Returns:
            answer: response to user query
        """
        context, _ = self.vector_db.hybrid_search(query=user_query)
        response = answer_chain.invoke(
            {
                "user_query": user_query,
                "uploaded_content": uploaded_content,
                "context": context,
                "chat_history": chat_history,
            }
        )
        return response

    def query_workflow(
        self,
        user_query: str,
        uploaded_content: str = "",
        chat_history: str = "",
    ) -> str:
        """
        complete workflow to generate response to user queries

        Returns:
            answer: response to user query
        """
        classification, reasoning, clarifying_question = self._router(
            user_query=user_query,
            uploaded_content=uploaded_content,
            chat_history=chat_history,
        )

        if classification == "unrelated":
            self.logger.info(f"route to `unrelated`")
            self.logger.info(f"reasoning: {reasoning}")
            return self.unrelated_response

        if classification == "vague":
            self.logger.info(f"route to `vague` with clarifying question")
            self.logger.info(f"reasoning: {reasoning}")
            return clarifying_question

        self.logger.info(f"route to `related`")
        return self._generate_answer(
            user_query=user_query,
            uploaded_content=uploaded_content,
            chat_history=chat_history,
        )

    def generate_email(
        self,
        chat_history: str,
    ) -> Tuple[str, str, List[str]]:
        """
        generates email template

        Returns:
            email_subject: email subject
            email_body: email body
            recipients: list of email recipients
        """
        result = generate_email_chain.invoke({"chat_history": chat_history})
        email_subject, email_body, email_recipients = (
            result.subject,
            result.body,
            result.recipients,
        )
        return email_subject, email_body, email_recipients
