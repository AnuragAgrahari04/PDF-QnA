import streamlit as st
import os
from ai_helper import PDFQuestionAnswerer

# Upload folder setup
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

def main():
    st.set_page_config(
        page_title="📄 PDF QnA App",
        layout="wide",
        page_icon="📚"
    )

    st.markdown("""
        <h1 style="text-align: center;">📚 Ask Questions from Your PDF</h1>
        <p style="text-align: center; font-size: 18px;">Upload your PDF and ask anything about it using AI-powered Q&A 💬</p>
    """, unsafe_allow_html=True)

    # Initialize session state
    if "pdf_qa" not in st.session_state:
        st.session_state.pdf_qa = PDFQuestionAnswerer()
    if "pdf_processed" not in st.session_state:
        st.session_state.pdf_processed = False
    if "search_history" not in st.session_state:
        st.session_state.search_history = []

    # --- Sidebar ---
    with st.sidebar:
        st.header("📤 Upload Your PDF")
        uploaded_file = st.file_uploader("Choose a PDF", type="pdf")

        if uploaded_file:
            file_path = os.path.join(UPLOAD_DIR, uploaded_file.name)
            with open(file_path, "wb") as f:
                f.write(uploaded_file.read())

            if st.button("⚙️ Process PDF"):
                with st.spinner("🔄 Embedding and indexing your document..."):
                    try:
                        num_chunks = st.session_state.pdf_qa.load_and_process_pdf(file_path)
                        st.session_state.pdf_processed = True
                        st.success(f"✅ Processed PDF into {num_chunks} chunks!")
                    except Exception as e:
                        st.error(f"❌ Error: {e}")

        st.header("🕘 Search History")
        if st.session_state.search_history:
            for idx, (q, a) in enumerate(st.session_state.search_history, 1):
                with st.expander(f"📌 {idx}. {q}"):
                    st.markdown(f"**🧠 Answer:** {a}")
            if st.button("🗑️ Clear History"):
                st.session_state.search_history = []
                st.experimental_rerun()
        else:
            st.info("No searches yet. Upload a PDF and start asking! 📄❓")

    # --- Main Interface ---
    st.subheader("🔍 Ask a Question")
    question = st.text_input("💬 What would you like to ask?", placeholder="e.g., What is the USP of Hackathon?")

    if st.button("🚀 Get Answer"):
        if not st.session_state.pdf_processed:
            st.warning("⚠️ Please upload and process a PDF first.")
        elif not question.strip():
            st.warning("✏️ Please enter a question.")
        else:
            with st.spinner("🤖 Thinking..."):
                try:
                    answer = st.session_state.pdf_qa.ask_question(question)
                    st.success("✅ Answer Generated!")
                    st.markdown(f"### 🧠 Answer:\n> {answer}")
                    st.session_state.search_history.append((question, answer))
                except Exception as e:
                    st.error(f"❌ Error: {e}")

    st.markdown("---")
    st.markdown(
        "<p style='text-align: center; font-size: 14px;'>🚀 Built with ❤️ using Streamlit and Cohere",
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()
