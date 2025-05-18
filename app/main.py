# app/main.py

import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
if st.session_state.history:
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.set_font("Arial", size=12)

    for i, chat in enumerate(st.session_state.history, 1):
        # Remove emojis to avoid encoding issues
        question_text = f"Question {i}: {chat['q']}".encode('latin1', 'replace').decode('latin1')
        answer_text = f"Answer:\n{chat['a']}".encode('latin1', 'replace').decode('latin1')
        
        pdf.set_font("Arial", size=12, style="B")
        pdf.multi_cell(0, 10, question_text)
        pdf.set_font("Arial", size=12)
        pdf.multi_cell(0, 10, answer_text)
        pdf.set_font("Arial", size=12, style="I")
        pdf.multi_cell(0, 10, "Sources:")
        
        for j, src in enumerate(chat['src'], 1):
            safe_src = f"{j}. {src.strip()}".encode('latin1', 'replace').decode('latin1')
            pdf.multi_cell(0, 8, safe_src)
        pdf.ln(5)

    # Output PDF to memory buffer
    pdf_bytes = pdf.output(dest='S').encode('latin1', 'replace')
    pdf_buffer = io.BytesIO(pdf_bytes)

    st.download_button(
        label="⬇️ Download Chat as PDF",
        data=pdf_buffer,
        file_name="legal_chat_session.pdf",
        mime="application/pdf"
    )
