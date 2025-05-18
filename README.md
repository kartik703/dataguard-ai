# 🛡️ DataGuard AI — Your Virtual Data Protection Officer

**DataGuard AI** is a smart legal assistant that leverages GPT-4 and vector search to answer compliance questions related to **UK GDPR**, **CCPA**, **HIPAA**, and **ICO** guidance.  
It helps startups, schools, clinics, and small businesses get reliable, source-backed answers to regulatory questions — instantly.

---

## 🚀 Live Demo

**👉 [Try the Hugging Face demo](https://huggingface.co/spaces/kartik703/dataguard-ai)** (Streamlit)

---

## 🧠 Features

- 💬 GPT-4 legal Q&A with semantic search (RAG)
- 📚 Source citations with every answer
- 🧠 Memory for follow-up questions
- 📄 Export entire chat session as PDF
- ⚠️ Disclaimer included (Not legal advice)

---

## 📁 Project Structure

```
dpai_app/
├── app/                # Streamlit frontend
│   └── main.py
├── backend/            # RAG pipeline
│   └── rag_pipeline.py
├── data/               # Legal corpus (GDPR, CCPA, HIPAA)
├── vector_store/       # FAISS index and source tracking
├── requirements.txt    # All Python dependencies
├── .env.example        # Add your OpenAI key here
└── README.md
```

---

## 🛠️ How to Run Locally

### 1. Clone the repo

```bash
git clone https://github.com/kartik703/dataguard-ai.git
cd dataguard-ai
```

### 2. Create and activate a virtual environment

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 3. Set your OpenAI API Key

Create a `.env` file and add:

```env
OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

### 4. Run the app

```bash
streamlit run app/main.py
```

---

## ☁️ Deploy to Hugging Face Spaces

1. Go to [Hugging Face Spaces](https://huggingface.co/spaces)
2. Create new Space (SDK: Streamlit)
3. Add your `OPENAI_API_KEY` in Settings → Secrets
4. Set app path to `app/main.py`

---

## 💡 Roadmap

- ✅ GPT-based Q&A
- ✅ PDF Export
- ✅ Multi-turn memory
- ⏳ Policy Analyzer (coming)
- 📢 Regulation alert system (planned)
- 📎 Slack/Email integrations (planned)

---

## 👤 About the Author

**Kartik Goswami**  
MSc Data Science & AI, Newcastle University  
GitHub: [@kartik703](https://github.com/kartik703)

---

## 📃 License

MIT — use it freely, give credit, and build something better!