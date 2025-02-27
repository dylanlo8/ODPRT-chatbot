QA_PROMPT = """You are an assistant that extracts all relevant question-answer pairs from a FAQ document.

faq_thread:
{faq_thread}

Instructions:
1. Identify all distinct questions.
2. Extract the corresponding answers, ensuring relevance and accuracy.
3. Maintain the chronological order of the questions and answers.
4. If no clear question is present, return an empty list for `questions`.

Output Format:
`questions`: ["First extracted question", "Second extracted question", ...],
`answers`: ["First corresponding answer", "Second corresponding answer", ...]"""