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

        # For PDFs, each page is converted into PNG bytes (how PNG images are stored in hard disk).
        # Gemini Vision needs image inputs, so we convert all pages to PNG.
        # pdf_to_images() returns a list of PNG byte data for each page.
        # These PNG bytes are sent to Gemini Vision as image objects.
        if "pdf" in file_type.lower() or file_name.lower().endswith(".pdf"):
            pages = self.pdf_converter.pdf_to_images(uploaded_file)
            prepared_images = [self.image_preparer.prepare_image(p) for p in pages]
            return self.gemini.ask(question, images=prepared_images)

        # Otherwise images in JPEG/PNG
        # For JPG/PNG uploads, Streamlit gives the file as raw bytes.
        # We extract those bytes using getvalue().
        # prepare_image() wraps these bytes as a Gemini-compatible image object.(PNG bytes)
        # The wrapped image bytes are then sent to Gemini Vision.
        img_bytes = uploaded_file.getvalue()
        prepared = self.image_preparer.prepare_image(img_bytes)
        return self.gemini.ask(question, images=[prepared])


# BACKWARD-COMPATIBLE FUNCTION (for app.py)
def process_invoice_qa(uploaded_file, question):
    """
    Connects Inputs and Backend.
    """
    processor = InvoiceProcessor()
    return processor.process(uploaded_file, question)
