import os

from langchain_openai import ChatOpenAI

gpt_4o_mini = ChatOpenAI(
    api_key=os.getenv('OPENAI_KEY'),
    model=os.getenv('OPENAI_MODEL'),
    temperature=0
)