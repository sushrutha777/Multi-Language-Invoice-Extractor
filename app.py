import streamlit as st
from backend.extract_pipeline import process_invoice_qa
from PIL import Image
from datetime import datetime

# Page setup
st.set_page_config(page_title="Invoice Q&A System", layout="wide")


def init_session_state():
    """Initialize session state for invoice Q&A history."""
    # history: list of dicts {id, question, answer, created_at, file_name}
    if "history" not in st.session_state:
        st.session_state.history = []
    # currently selected history index (0-based), None if nothing selected
    if "selected_history_index" not in st.session_state:
        st.session_state.selected_history_index = None


def render_history_entry(idx: int | None):
    """Show selected Q&A from history in the main area."""
    if idx is None:
        return

    if idx < 0 or idx >= len(st.session_state.history):
        st.error("Selected history item not found.")
        return

    item = st.session_state.history[idx]
    st.markdown("---")
    st.markdown(
        f"### Previous Q&A — {item['created_at'].strftime('%Y-%m-%d %H:%M:%S')}"
    )
    if item.get("file_name"):
        st.caption(f"📄 Invoice: {item['file_name']}")
    st.markdown(f"**Question:** {item['question']}")
    st.markdown("**Answer:**")
    st.write(item["answer"])


def main():
    init_session_state()
    st.title("Multi-Language Invoice Q&A System")
    # Sidebar: HISTORY
    with st.sidebar:
        st.markdown("## History")
        if st.session_state.history:
            labels = []
            for idx, item in enumerate(reversed(st.session_state.history)):
                original_id = len(st.session_state.history) - idx  # 1-based
                q = item["question"]
                label = f"{original_id}. {q[:60]}{'...' if len(q) > 60 else ''}"
                labels.append(label)

            choice = st.selectbox(
                "Select a previous question",
                options=["(none)"] + labels,
                index=0,
            )

            if choice != "(none)":
                num_str = choice.split(".", 1)[0]
                try:
                    orig_idx = int(num_str) - 1  # zero-based
                    st.session_state.selected_history_index = orig_idx
                except Exception:
                    st.session_state.selected_history_index = None
            else:
                st.session_state.selected_history_index = None

            if st.button("Clear history"):
                st.session_state.history = []
                st.session_state.selected_history_index = None
                st.rerun()
        else:
            st.info("No history yet. Ask a question after uploading an invoice.")

    # Upload Section
    uploaded_file = st.file_uploader(
        "Upload an Invoice (PDF, JPG, JPEG, PNG)",
        type=["pdf", "jpg", "jpeg", "png"],
    )

    # Display preview if image
    if uploaded_file is not None and uploaded_file.type != "application/pdf":
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Invoice", use_container_width=True)

    # Show selected history Q&A (if any)
    selected_idx = st.session_state.get("selected_history_index", None)
    render_history_entry(selected_idx)

    # Question Input (current invoice)
    if uploaded_file is not None:
        user_question = st.text_input(
            "Ask your question about this invoice",
            key="invoice_question",
            placeholder="e.g., What is the total amount? Who is the vendor?",
        )

        if st.button("Ask Question"):
            if not user_question.strip():
                st.warning("Please type a question first.")
            else:
                with st.spinner("Thinking..."):
                    try:
                        answer = process_invoice_qa(uploaded_file, user_question)
                        st.subheader("Answer")
                        st.write(answer)

                        # Save to history
                        entry = {
                            "id": len(st.session_state.history) + 1,
                            "question": user_question.strip(),
                            "answer": answer,
                            "file_name": getattr(uploaded_file, "name", None),
                            "created_at": datetime.now(),
                        }
                        st.session_state.history.append(entry)
                        st.session_state.selected_history_index = entry["id"] - 1
                    except Exception as e:
                        st.error(f"Error: {str(e)}")
    else:
        st.info("Please upload your invoice to get started.")


if __name__ == "__main__":
    main()
