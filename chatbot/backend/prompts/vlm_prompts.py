IMAGE_SUMMARY_PROMPT = "Generate me a summary of this image in less than 150 words."

FILTER_IMAGE_PROMPT = """Assess the image for relevance to research grant administration. Useful images include charts, graphs, diagrams, and research-related visuals. Non-useful images include clipart, decorative graphics, stock icons, and unrelated objects.  

Instructions:  
- Briefly justify your classification.  
- Categorize as:  
  1. Useful: Contains research-relevant data (e.g., visualizations, organizational charts).  
  2. Not Useful: Lacks research value (e.g., clipart, decorative elements, generic images).
- Return the classification and justification in a JSON format, without any preambles or additional text.

Example Output:
{{
    "justification": "The image contains a bar graph depicting research funding trends over five years, relevant to grant administration"
    "classification": "Useful"
}}
"""

RELEVANCE_CLASSIFICATION_PROMPT = """
Given an email context, determine if the image is relevant to the email. The attachment into images for your classification.

Guidelines for Classification:
1. Relevant: The attachment contains specific, actionable, or relevant information regarding that supplements the given email context.
2. Not relevant: The attachment is generic, lacks substantive content, or does not align with the email context.
3. Not relevant: If no clear determination can be made, classify as "Not relevant."

Instructions:
1. Read the email thread.
2. Read the extract images.
3. Write a brief and concise reasoning for your classification.
4. Classify the attachment as "relevant" or "not_relevant."

Example Output:
{{
    "justification": "(Brief and concise explanation)"
    "classification": "relevant"
}}
"""

