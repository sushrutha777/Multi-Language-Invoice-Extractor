def prepare_image(uploaded_file):
    """Converting uploaded image to proper format for Gemini"""
    bytes_data = uploaded_file.getvalue()
    image_parts = [{
        "mime_type": uploaded_file.type,
        "data": bytes_data
    }]
    return image_parts[0]
