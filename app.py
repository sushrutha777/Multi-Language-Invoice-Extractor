import streamlit as st
from backend.extract_pipeline import process_invoice_qa
from PIL import Image

# Page setup
st.set_page_config(page_title="Invoice Q&A System", layout="wide")

st.title("Multi-Language Invoice Q&A System")

# ---- Initialize conversation history ----
if "qa_history" not in st.session_state:
    # each item will be {"question": ..., "answer": ...}
    st.session_state.qa_history = []

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

    # --- Show previous Q&A history ---
    if st.session_state.qa_history:
        st.subheader("Conversation so far")
        for qa in st.session_state.qa_history:
            st.markdown(f"**You:** {qa['question']}")
            st.markdown(f"**Answer:** {qa['answer']}")
            st.markdown("---")

    # Current question input
    user_question = st.text_input(
        "Ask your question about this invoice",
        key="question_input"
    )

    if st.button("Ask Question"):
        if not user_question.strip():
            st.warning("Please type a question first.")
        else:
            with st.spinner("Thinking..."):
                try:
                    answer = process_invoice_qa(uploaded_file, user_question)

                    # Save this Q&A to history so it doesn't disappear
                    st.session_state.qa_history.append({
                        "question": user_question,
                        "answer": answer
                    })
                except Exception as e:
                    st.error(f"Error: {str(e)}")
else:
    st.info("Please upload your invoice to get started.")
