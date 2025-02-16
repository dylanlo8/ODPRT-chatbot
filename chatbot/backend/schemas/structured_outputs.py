from pydantic import BaseModel, Field
from typing import Literal, List


class UsefulnessClassification(BaseModel):
    reasoning: str = Field(description="The reasoning behind the classification")
    classification: Literal["useful", "not_useful"] = Field(
        description="a string to represent if the thread is useful or not useful"
    )


class QAPairs(BaseModel):
    questions: List[str] = Field(
        description="A list of question(s) the client(s) is/are asking"
    )
    answers: List[str] = Field(description="The answers to the question(s) asked")


class SemanticRouting(BaseModel):
    answer: str = Field(description="The answer to the user query")
    classification: Literal["VAGUE", "NOT_RELATED", "RELATED"] = Field(
        description="a string to represent if the query is vague, not related or related"
    )
