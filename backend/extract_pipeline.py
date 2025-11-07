from backend.pdf_utils import extract_text_from_pdf
from backend.image_utils import prepare_image
from backend.gemini_utils import ask_gemini_about_invoice

def process_invoice_qa(uploaded_file, user_question):
    """Processes uploaded invoices (PDF or image) and gets Gemini's answer."""

    file_type = uploaded_file.type
    if "pdf" in file_type:
        # Extract text from PDF
        text_data = extract_text_from_pdf(uploaded_file)
        if not text_data.strip():
            raise ValueError("No readable text found in PDF.")
        return ask_gemini_about_invoice(user_question, text_data=text_data)
    else:
        # Prepare image for Gemini Vision
        image_data = prepare_image(uploaded_file)
        return ask_gemini_about_invoice(user_question, image_data=image_data)
