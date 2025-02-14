from chatbot.backend.schemas.structured_outputs import UsefulnessClassification, QAPairs
from chatbot.backend.services.models.llm import gpt_4o_mini

classification_chain = ChatPromptTemplate([
    ("system", CLASSIFICATION_PROMPT),
    ("human", "{email_thread}"),
]) | gpt_4o_mini.with_structured_output(UsefulnessClassification)


qa_chain = ChatPromptTemplate([
    ("system", QA_PROMPT),
    ("human", "{email_thread}"),
]) | gpt_4o_mini.with_structured_output(QAPairs)
