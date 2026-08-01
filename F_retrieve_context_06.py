"""06_retrieve_context.py — Retrieve relevant stanzas from ChromaDB."""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import importlib
vectors = importlib.import_module("04_vector_representation")
store   = importlib.import_module("05_create_chroma_store")

embed_query          = vectors.embed_query
get_or_build_collection = store.get_or_build_collection

_collection = None


def _get_collection():
    global _collection
    if _collection is None:
        _collection = get_or_build_collection()
    return _collection


def retrieve(query, k=4, min_score=0.25):
    collection     = _get_collection()
    query_embedding = embed_query(query).tolist()
    raw = collection.query(
        query_embeddings=[query_embedding],
        n_results=min(k, collection.count()),
        include=["documents", "metadatas", "distances"],
    )
    results = []
    for doc, meta, dist in zip(
        raw["documents"][0],
        raw["metadatas"][0],
        raw["distances"][0],
    ):
        score = round(1.0 - float(dist), 4)
        if score < min_score:
            continue
        results.append({
            "chunk_id":       meta["chunk_id"],
            "section_number": meta["section_number"],
            "section_title":  meta["section_title"],
            "stanza_label":   meta["stanza_label"],
            "first_line":     meta["first_line"],
            "text":           doc,
            "score":          score,
        })
    results.sort(key=lambda r: r["score"], reverse=True)
    return results


def build_context_string(results):
    if not results:
        return "No relevant passages found in the poem."
    blocks = []
    for i, r in enumerate(results, 1):
        blocks.append(f"[Source {i} -- {r['stanza_label']}]\n{r['text']}")
    return "\n\n".join(blocks)


def retrieve_and_format(query, k=4):
    results = retrieve(query, k=k)
    context = build_context_string(results)
    return results, context


if __name__ == "__main__":
    for q in ["What does the thunder say?", "Who is Tiresias?"]:
        print(f"\nQUERY: {q}")
        results, _ = retrieve_and_format(q, k=3)
        for r in results:
            print(f"  [{r['score']:.3f}] {r['stanza_label']}")
