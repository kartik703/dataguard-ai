# backend/rag_pipeline.py

import faiss
import os
from sentence_transformers import SentenceTransformer
from dotenv import load_dotenv
import openai

# Load environment variables
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
client = openai.OpenAI(api_key=OPENAI_API_KEY)

# Paths and constants
INDEX_PATH = "vector_store/faiss_index.idx"
SOURCE_PATH = "vector_store/sources.txt"
EMBED_MODEL = "all-MiniLM-L6-v2"

def load_index_and_sources():
    """Load FAISS index and corresponding text chunks."""
    index = faiss.read_index(INDEX_PATH)
    with open(SOURCE_PATH, "r", encoding="utf-8") as f:
        sources = f.readlines()
    return index, sources

def embed_query(query, model):
    """Convert the question into a vector using sentence transformer."""
    return model.encode([query])[0]

def retrieve_context(query, k=3):
    """Semantic search: retrieve top-k similar chunks based on the query."""
    model = SentenceTransformer(EMBED_MODEL)
    index, sources = load_index_and_sources()
    query_vec = embed_query(query, model)

    D, I = index.search(query_vec.reshape(1, -1), k * 3)  # broaden retrieval
    raw_results = [sources[i].strip() for i in I[0]]

    query_lower = query.lower()
    if "uk" in query_lower or "gdpr" in query_lower:
        results = [r for r in raw_results if "[UK_GDPR]" in r or "[ICO]" in r]
    elif "ccpa" in query_lower:
        results = [r for r in raw_results if "[CCPA]" in r]
    elif "hipaa" in query_lower:
        results = [r for r in raw_results if "[HIPAA]" in r]
    else:
        results = raw_results

    return results[:k]

def query_gpt(context, question):
    """Send the context and question to GPT-4 to generate a legal answer."""
    prompt = f"""You are a legal assistant specializing in global data protection laws.

Using the context below, answer the user's question clearly and accurately.

Context:
{context}

Question: {question}
"""

    response = client.chat.completions.create(
        model="gpt-4",  # use "gpt-3.5-turbo" if needed
        messages=[
            {"role": "system", "content": "You are a compliance assistant for data protection law (GDPR, CCPA, HIPAA)."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.3,
    )

    return response.choices[0].message.content.strip()

def evaluate_hallucination(answer, context):
    """Optional: Check if GPT hallucinated any part of the answer."""
    prompt = f"""You are a legal evaluator.

Check if the following answer contains any statements that are NOT supported by the context. Be specific.

Answer:
{answer}

Context:
{context}

Respond with either:
✅ Supported  
⚠️ Hallucination Detected: <short explanation>
"""

    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0
    )
    return response.choices[0].message.content.strip()

def ask_question(question, previous=None):
    """Main function: Retrieve context, generate GPT answer, and return both."""
    context_chunks = retrieve_context(question)
    combined_context = "\n\n".join(context_chunks)

    if previous:
        combined_context = previous + "\n\n---\n\n" + combined_context

    answer = query_gpt(combined_context, question)

    # Optional: add hallucination checker
    # flag = evaluate_hallucination(answer, combined_context)
    # print("Hallucination check:", flag)

    return answer, context_chunks
