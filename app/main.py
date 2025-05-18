# app/main.py

import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from backend.rag_pipeline import ask_question
import streamlit as st
from fpdf import FPDF
import io

st.set_page_config(page_title="🛡️ Data Protection AI Assistant", layout="wide")

# ───────────── Legal Disclaimer ─────────────
st.warning("⚠️ This assistant provides general legal information and should not be considered a substitute for professional legal advice.")

# ───────────── Chat History State ─────────────
if "history" not in st.session_state:
    st.session_state.history = []

# ───────────── Page Header ─────────────
st.title("🛡️ AI Legal Assistant for Data Protection")
st.markdown("Ask legal questions about **UK GDPR**, **ICO**, **CCPA**, or **HIPAA** regulations.")

# ───────────── Input ─────────────
question = st.text_input("🔍 Enter your legal question:")

if question:
    with st.spinner("Thinking..."):
        # Combine previous Q&A as memory
        previous_context = "\n\n".join(
            f"Q: {entry['q']}\nA: {entry['a']}"
            for entry in st.session_state.history
        ) if st.session_state.history else None

        answer, sources = ask_question(question, previous=previous_context)
        st.session_state.history.append({"q": question, "a": answer, "src": sources})

# ───────────── Display History ─────────────
for i, chat in enumerate(reversed(st.session_state.history), 1):
    st.markdown(f"### ❓ Question {len(st.session_state.history) - i + 1}")
    st.markdown(f"> {chat['q']}")
    st.markdown("**🧠 GPT Answer:**")
    st.success(chat['a'])

    with st.expander("📚 Sources Used"):
        for j, src in enumerate(chat['src'], 1):
            st.markdown(f"**Source {j}:**")
            st.code(src.strip())

# ───────────── PDF Export Button ─────────────
if st.session_state.history:
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.set_font("Arial", size=12)

    for i, chat in enumerate(st.session_state.history, 1):
        pdf.set_font("Arial", size=12, style="B")
        pdf.multi_cell(0, 10, f"Question {i}: {chat['q']}")
        pdf.set_font("Arial", size=12, style="")
        pdf.multi_cell(0, 10, f"Answer:\n{chat['a']}")
        pdf.set_font("Arial", size=12, style="I")
        pdf.multi_cell(0, 10, "Sources:")
        for j, src in enumerate(chat['src'], 1):
            pdf.multi_cell(0, 8, f"{j}. {src.strip()}")
        pdf.ln(5)

    # Output PDF to memory buffer
    pdf_bytes = pdf.output(dest='S').encode('latin1')
    pdf_buffer = io.BytesIO(pdf_bytes)

    st.download_button(
        label="⬇️ Download Chat as PDF",
        data=pdf_buffer,
        file_name="legal_chat_session.pdf",
        mime="application/pdf"
    )
