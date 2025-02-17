CLASSIFICATION_PROMPT = """You are a classification assistant determining whether an email thread is useful or not.

Email Thread:
{email_thread}

Context:
The NUS Office of the Deputy President (Research & Technology) (ODPRT) oversees research compliance, integrity, grant administration, strategic initiatives, industry engagement, and research communications at NUS. The Industry Engagements & Partnerships (IEP) team within ODPRT manages industry partnerships and collaborations.

Guidelines for Classification:
1. Useful: The thread contains specific, actionable, or relevant information regarding research funding, industry partnerships, or strategic initiatives.
2. Not Useful: The thread is generic, lacks substantive content, or does not pertain to ODPRT's functions.
3. Not Useful: If no clear determination can be made, classify as "Not Useful."

Instructions:
1. Read the email thread.
2. Write a brief and concise reasoning for your classification.
3. Classify the email thread as "useful" or "not_useful."

Output Format:
- `reasoning`: (Brief and concise explanation)
- `classification`: 'useful' or 'not_useful'"""

QA_PROMPT = """You are an assistant that extracts all relevant question-answer pairs from an email thread.

Email Thread:
{email_thread}

Instructions:
1. Identify all distinct questions asked by the sender(s) within the email thread.
2. Extract the corresponding answers from the same thread, ensuring relevance and accuracy.
3. Add context wherever necessary to provide a clear and concise question-answer pair.
4. Maintain the chronological order of the questions and answers.
5. If no clear question is present, return an empty list for `questions`.
6. If a question has no available answer in the thread, return "No answer available" in the corresponding position in `answers`.

Output Format:
`questions`: ["First extracted question", "Second extracted question", ...],
`answers`: ["First corresponding answer", "Second corresponding answer", ...]"""