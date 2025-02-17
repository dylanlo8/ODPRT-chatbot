from pydantic import BaseModel, Field
from typing import Literal, List


class UsefulnessClassification(BaseModel):
    reasoning: str = Field(description="The reasoning behind the classification")
    classification: Literal["useful", "not_useful"] = Field(
        description="a string to represent if the thread is useful or not useful"
    )

class RelevanceClassification(BaseModel):
    reasoning: str = Field(description="The reasoning behind the classification")
    classification: Literal["relevant", "not_relevant"] = Field(
        description="a string to represent if the attachment is relevant or not relevant to the email context"
    )

class QAPairs(BaseModel):
    questions: List[str] = Field(
        description="A list of question(s) the client(s) is/are asking"
    )
    answers: List[str] = Field(description="The answers to the question(s) asked")


class SemanticRouting(BaseModel):
    classification: Literal["not_related", "related", "vague"] = Field(
        description="a string to represent if the query is vague, not related or related"
    )
    clarifying_question: str = Field(
        description="A follow-up question to request more details before proceeding with further classification."
    )
