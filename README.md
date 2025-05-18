# 🛡️ AI Data Protection Consultant

An interactive legal assistant that answers questions about GDPR, CCPA, HIPAA, and ICO regulations using GPT-4 and FAISS-based semantic search.

## Features
- GPT-4-powered legal Q&A
- Sources from real data protection laws
- Session memory for follow-ups
- PDF export of conversations

## Deployment

### Streamlit Cloud
1. Push this repo to GitHub.
2. Go to [streamlit.io/cloud](https://streamlit.io/cloud), sign in with GitHub.
3. Click "New app", select your repo and `app/main.py`.

### Hugging Face Spaces
1. Go to [Hugging Face Spaces](https://huggingface.co/spaces).
2. Create a new space (type: Streamlit).
3. Upload all your project files and `requirements.txt`.

---

## ⚠️ Environment Variable
Make sure to add your `OPENAI_API_KEY` as a secret:
- **Streamlit Cloud**: Settings > Secrets
- **Hugging Face**: Secrets tab (`OPENAI_API_KEY`)

