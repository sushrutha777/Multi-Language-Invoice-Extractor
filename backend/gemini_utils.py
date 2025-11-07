import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_gemini_response(prompt, image_data=None, text_data=None):
    """Generates a Gemini response using either vision or text model."""
    model = genai.GenerativeModel("gemini-pro-vision" if image_data else "gemini-pro")

    if image_data:
        response = model.generate_content([prompt, image_data])
    else:
        response = model.generate_content(f"{prompt}\n\n{text_data}")

    return response.text

def ask_gemini_about_invoice(prompt, text_data=None, image_data=None):
    # Choose a valid model
    model_name = "gemini-2.5-flash"  # check list_models to confirm access
    model = genai.GenerativeModel(model_name)

    if image_data:
        response = model.generate_content([prompt, image_data])
    else:
        response = model.generate_content(f"{prompt}\n\n{text_data}")

    return response.text

