import streamlit as st
from backend.extract_pipeline import process_invoice_qa
from PIL import Image

# Page setup
st.set_page_config(page_title="Invoice Q&A System", layout="wide")

st.title("Multi-Language Invoice Q&A System")

# Upload Section
uploaded_file = st.file_uploader(
    "Upload an Invoice (PDF, JPG, JPEG, PNG)",
    type=["pdf", "jpg", "jpeg", "png"]
)

# Display preview if image
if uploaded_file is not None and uploaded_file.type != "application/pdf":
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Invoice", use_container_width=True)

# Question input comes AFTER upload preview
if uploaded_file is not None:
    user_question = st.text_input("Ask your question about this invoice')")

    if st.button("Ask Question"):
        if not user_question.strip():
            st.warning("Please type a question first.")
        else:
            with st.spinner("Thinking..."):
                try:
                    answer = process_invoice_qa(uploaded_file, user_question)
                    st.subheader("Answer")
                    st.write(answer)
                except Exception as e:
                    st.error(f"Error: {str(e)}")
else:
    st.info("Please upload your invoice to get started.")