# backend/pdf_utils.py
import fitz  # PyMuPDF

class PDFToImageConverter:
    """Converts PDF pages into high-quality images for vision models."""

    def __init__(self, dpi: int = 200):
        self.dpi = dpi

    def pdf_to_images(self, file_like):
        """Returns list of image bytes for each page."""
        # Open PDF (path or uploaded file)
        if isinstance(file_like, str):
            doc = fitz.open(file_like)
        else:
            file_like.seek(0)
            doc = fitz.open(stream=file_like.read(), filetype="pdf")

        images = []
        for page in doc:
            pix = page.get_pixmap(matrix=fitz.Matrix(self.dpi/72, self.dpi/72))
            images.append(pix.tobytes("png"))

        doc.close()
        return images
