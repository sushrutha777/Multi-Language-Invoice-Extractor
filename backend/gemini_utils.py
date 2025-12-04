# backend/gemini_utils.py
import google.generativeai as genai
import os
from dotenv import load_dotenv

class GeminiClient:
    def __init__(self):
        load_dotenv()
        genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

    def ask(self, prompt, images=None):
        # Always use Gemini Vision model
        model = genai.GenerativeModel("gemini-2.5-pro")
        if images:
            payload = [prompt] + images
            response = model.generate_content(payload)
            return response.text
        # If for some reason images is empty
        return "No images provided for analysis."

