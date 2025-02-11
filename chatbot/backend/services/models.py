import base64
import os
import requests
from io import BytesIO
from PIL import Image
from dotenv import load_dotenv

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

    def generate_image_summaries(self, image_paths):
        summaries = []
        for image_path in image_paths:
            img = Image.open(image_path)
            base64_img = self.encode_image(img)
            payload = {
                "messages": [
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": "Generate me a summary of this image."},
                            {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_img}"}},
                        ],
                    }
                ],
                "model": "Qwen/Qwen2-VL-7B-Instruct",
                "max_tokens": 300,
                "temperature": 0.1,
                "top_p": 0.9,
            }
            response = requests.post(self.api, headers=self.headers, json=payload)
            summary = response.json().get("choices", [{}])[0].get("message", {}).get("content", "No summary available")
            summaries.append(summary)
        return summaries
    
vlm = VLM()