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


