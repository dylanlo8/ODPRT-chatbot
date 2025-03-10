IMAGE_SUMMARY_PROMPT = "Generate me a summary of this image in less than 150 words."

FILTER_IMAGE_PROMPT = """Assess the image for relevance to research grant administration. Useful images include full tables, charts, graphs, diagrams, and research-related visuals. 

Non-useful images include:
- Clipart, decorative graphics, stock icons, logos.
- Empty table cells, small table fragments, isolated numbers, or isolated labels without context.
- Generic headers, section dividers, timestamps, metadata and table headers without context.
- Contract related fields, Signature fields, signature-like elements, and authorization stamps.
- Contract Events

**Instructions:**  
- Provide a brief justification for your classification.  
- Categorize the image as either:  
  1. `"Useful"`: The image contains structured tabular data, figures, or research-relevant visuals.  
  2. `"Not Useful"`: The image lacks meaningful research context (e.g., isolated numbers, decorative elements, logos, signatures).

**Example Outputs:**
```json
{
    "justification": "This image contains a detailed budget table with labeled headers and multiple data points, making it relevant to grant administration.",
    "classification": "Useful"
}

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

