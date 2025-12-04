# backend/gemini_utils.py
import google.generativeai as genai
import os
from dotenv import load_dotenv

class GeminiClient:
    def __init__(self):
        load_dotenv()
        genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

    def ask(self, prompt, images=None, text_data=None):
        model = genai.GenerativeModel("gemini-2.5-pro" if images else "gemini-2.5-flash")

        if images:
            payload = [prompt] + images
            response = model.generate_content(payload)
        else:
            response = model.generate_content(prompt)

        return response.text
