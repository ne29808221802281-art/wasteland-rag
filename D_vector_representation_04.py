"""04_vector_representation.py — Encode chunks with multilingual-MiniLM-L12-v2."""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import numpy as np
import importlib
chunking = importlib.import_module("03_chunking")
get_chunks = chunking.get_chunks

MODEL_NAME = "paraphrase-multilingual-MiniLM-L12-v2"
_model = None


def get_model():
    global _model
    if _model is None:
        from sentence_transformers import SentenceTransformer
        print(f"Loading model: {MODEL_NAME}")
        _model = SentenceTransformer(MODEL_NAME)
    return _model


def embed_texts(texts):
    model = get_model()
    return model.encode(
        texts,
        batch_size=32,
        convert_to_numpy=True,
        normalize_embeddings=True,
        show_progress_bar=True,
    )


def embed_query(query):
    model = get_model()
    vec = model.encode(
        [query],
        convert_to_numpy=True,
        normalize_embeddings=True,
    )
    return vec[0]


def get_chunk_embeddings(chunks=None):
    if chunks is None:
        chunks = get_chunks()
    texts = [c["search_text"] for c in chunks]
    embeddings = embed_texts(texts)
    return chunks, embeddings


if __name__ == "__main__":
    chunks, embeddings = get_chunk_embeddings()
    print(f"Chunks: {len(chunks)}, Embed shape: {embeddings.shape}")
    print(f"First vec norm: {np.linalg.norm(embeddings[0]):.4f}")
