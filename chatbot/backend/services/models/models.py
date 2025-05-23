import base64
import json
import os
import requests

from dotenv import load_dotenv
from io import BytesIO
from typing import List
from PIL import Image

from chatbot.backend.prompts.vlm_prompts import IMAGE_SUMMARY_PROMPT, FILTER_IMAGE_PROMPT, RELEVANCE_CLASSIFICATION_PROMPT

class VLM:
    def __init__(self):
        load_dotenv()
        
        self.api_key = os.getenv("HYPERBOLIC_API_KEY")
        self.api = "https://api.hyperbolic.xyz/v1/chat/completions"
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}",
        }

    def encode_image(self, img):
        buffered = BytesIO()
        img.save(buffered, format="PNG")
        return base64.b64encode(buffered.getvalue()).decode("utf-8")
    
    def _build_payload(self, 
                        prompt: str, 
                        image_path: str):
        img = Image.open(image_path)
        base64_img = self.encode_image(img)
        payload = {
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt},
                        {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_img}"}},
                    ],
                }
            ],
            "model": "Qwen/Qwen2-VL-7B-Instruct",
            "max_tokens": 300,
            "temperature": 0.1,
            "top_p": 0.9,
        }
        return payload
    
    def _build_payloads_for_attachments(self, 
                   email_context: str, 
                   extracted_images: List[str]):
        payloads = []
        for image_path in extracted_images:
            img = Image.open(image_path)
            base64_img = self.encode_image(img)
            payload = {
                "messages": [
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": RELEVANCE_CLASSIFICATION_PROMPT},
                            {"type": "text", "text": f"Email Context:\n{email_context}"},
                            {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_img}"}},
                        ],
                    }
                ],
                "model": "Qwen/Qwen2-VL-7B-Instruct",
                "max_tokens": 300,
                "temperature": 0.1,
                "top_p": 0.9,
            }
            payloads.append(payload)
        return payloads
    
    def filter_images(self, 
                      image_paths: List[str],
                      prompt: str = FILTER_IMAGE_PROMPT) -> List[str]:
        """
        filters out images that are not useful for ingestion

        Args:
            image_paths (List[str]): list of image paths.

        Returns:
            useful_image_paths (List[str]): useful images only
        """
        useful_image_paths = []
        for image_path in image_paths:
            payload = self._build_payload(prompt=prompt, image_path=image_path)
            response = requests.post(self.api, headers=self.headers, json=payload)
            answer = response.json().get("choices", [{}])[0].get("message", {}).get("content", "No classification available")
            if answer == "No classification available":
                continue
            try:
                json_answer = json.loads(answer)
                classification, justification = json_answer.get("classification", "Not Useful"), json_answer.get("justification", "No justification provided")
                if classification == "Useful":
                    useful_image_paths.append(image_path)
                    print(justification)
            except json.JSONDecodeError:
                continue
        
        return useful_image_paths

    def generate_image_summaries(self, 
                                 useful_image_paths: List[str],
                                 prompt: str = IMAGE_SUMMARY_PROMPT) -> List[str]:
        """
        generate summaries for a list of images.

        Args:
            useful_image_paths (List[str]): list of useful image paths

        Returns:
            summaries (List[str]): list of summaries
        """
        summaries = []
        for image_path in useful_image_paths:
            payload = self._build_payload(prompt=prompt, image_path=image_path)
            response = requests.post(self.api, headers=self.headers, json=payload)
            summary = response.json().get("choices", [{}])[0].get("message", {}).get("content", "No summary available")
            if summary != "No summary available":
                summaries.append(summary)
        return summaries
    
vlm = VLM()