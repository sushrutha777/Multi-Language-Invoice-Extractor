# backend/image_utils.py
class ImagePreparer:
    def prepare_image(self, img_bytes):
        """Convert PNG bytes to Gemini-compatible format."""
        return {
            "mime_type": "image/png",
            "data": img_bytes
        }
