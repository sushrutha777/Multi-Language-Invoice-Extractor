import streamlit as st
from backend.extract_pipeline import process_invoice_qa
from PIL import Image

# Page setup
st.set_page_config(page_title="Invoice Q&A System", layout="wide")

st.title("Multi-Language Invoice Q&A System")

# --- Keep only the latest answer in session_state ---
if "last_answer" not in st.session_state:
    st.session_state.last_answer = None

# Upload Section
uploaded_file = st.file_uploader(
    "Upload an Invoice (PDF, JPG, JPEG, PNG)",
    type=["pdf", "jpg", "jpeg", "png"]
)

# Display preview if image
if uploaded_file is not None and uploaded_file.type != "application/pdf":
    image = Image.open(uploaded_file)
    # limit width so it doesn't take entire UI
    st.image(image, caption="Uploaded Invoice", width=400)

# Question input comes AFTER upload preview
if uploaded_file is not None:
    user_question = st.text_input("Ask your question about this invoice")

    if st.button("Ask Question"):
        if not user_question.strip():
            st.warning("Please type a question first.")
        else:
            with st.spinner("Thinking..."):
                try:
                    answer = process_invoice_qa(uploaded_file, user_question)
                    # store latest answer so it persists across reruns
                    st.session_state.last_answer = answer
                except Exception as e:
                    st.error(f"Error: {str(e)}")

    # Always show the latest answer (if any)
    if st.session_state.last_answer:
        st.subheader("Answer")
        st.write(st.session_state.last_answer)

else:
    st.info("Please upload your invoice to get started.")
