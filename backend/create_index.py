# backend/create_index.py

import os
import faiss
from sentence_transformers import SentenceTransformer
from tqdm import tqdm

DATA_FILES = [
    "data/uk_gdpr_articles.txt",
    "data/ico_guidance.txt",
    "data/ccpa.txt",
    "data/hipaa.txt"
]

OUTPUT_DIR = "vector_store"
CHUNK_SIZE = 500  # characters
EMBED_MODEL = "all-MiniLM-L6-v2"

def load_and_chunk(filepath):
    chunks = []
    with open(filepath, "r", encoding="utf-8") as f:
        text = f.read()
        parts = text.split("\n\n---\n\n") if "---" in text else text.split("\n\n")
        for part in parts:
            for i in range(0, len(part), CHUNK_SIZE):
                chunk = part[i:i+CHUNK_SIZE].strip()
                if len(chunk) > 50:
                    chunks.append((chunk, filepath))
    return chunks

def build_index():
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

    model = SentenceTransformer(EMBED_MODEL)

    corpus = []
    sources = []
    for file in DATA_FILES:
        print(f"📄 Loading {file}...")
        chunks = load_and_chunk(file)
        source_tag = os.path.basename(file).replace(".txt", "").upper()  # e.g., UK_GDPR
        for chunk, source in chunks:
            tagged_chunk = f"[{source_tag}]\n{chunk.strip()}"
            corpus.append(tagged_chunk)
            sources.append(tagged_chunk)

    print(f"🧠 Embedding {len(corpus)} chunks...")
    embeddings = model.encode(corpus, show_progress_bar=True)

    index = faiss.IndexFlatL2(embeddings.shape[1])
    index.add(embeddings)

    # Save index + chunks
    faiss.write_index(index, f"{OUTPUT_DIR}/faiss_index.idx")
    with open(f"{OUTPUT_DIR}/sources.txt", "w", encoding="utf-8") as f:
        for line in corpus:
            f.write(line.replace("\n", " ") + "\n")

    print(f"✅ FAISS index saved to: {OUTPUT_DIR}/faiss_index.idx")
    print(f"✅ Text chunks saved to: {OUTPUT_DIR}/sources.txt")

if __name__ == "__main__":
    build_index()
