# backend/extract_pipeline.py
from .pdf_utils import PDFToImageConverter
from .image_utils import ImagePreparer
from .gemini_utils import GeminiClient

class InvoiceProcessor:
    def __init__(self):
        self.pdf_converter = PDFToImageConverter()
        self.image_preparer = ImagePreparer()
        self.gemini = GeminiClient()

    def process(self, uploaded_file, question):
        file_type = getattr(uploaded_file, "type", "")
        file_name = getattr(uploaded_file, "name", "")

        # PDF → convert to images → send to Gemini Vision
        if "pdf" in file_type.lower() or file_name.lower().endswith(".pdf"):
            pages = self.pdf_converter.pdf_to_images(uploaded_file)
            prepared_images = [self.image_preparer.prepare_image(p) for p in pages]
            return self.gemini.ask(question, images=prepared_images)

        # Otherwise image
        img_bytes = uploaded_file.getvalue()
        prepared = self.image_preparer.prepare_image(img_bytes)
        return self.gemini.ask(question, images=[prepared])


# BACKWARD-COMPATIBLE WRAPPER FUNCTION (for app.py)

def process_invoice_qa(uploaded_file, question):
    """
    Wrapper so existing Streamlit code continues to work.
    """
    processor = InvoiceProcessor()
    return processor.process(uploaded_file, question)
