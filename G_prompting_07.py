"""07_prompting.py — Prompt builder and OpenRouter LLM call."""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import json
import urllib.request
import urllib.error
import importlib

retriever = importlib.import_module("06_retrieve_context")
retrieve_and_format = retriever.retrieve_and_format

OPENROUTER_API_KEY = os.environ.get("OPENROUTER_API_KEY", "")
OPENROUTER_MODEL   = os.environ.get("OPENROUTER_MODEL", "openai/gpt-4o-mini")
OPENROUTER_URL     = "https://openrouter.ai/api/v1/chat/completions"

SYSTEM_PROMPT = (
    "You are a scholarly literary assistant specialising in T. S. Eliot's poem "
    "The Waste Land (1922).\n\n"
    "Answer the user's question using ONLY the poem passages provided in the context.\n\n"
    "Rules:\n"
    "1. Use only the provided [Source N] passages. Do not add outside knowledge.\n"
    "2. Cite sources by number, e.g. [Source 1], [Source 2].\n"
    "3. Quote no more than 15 words from any single source; paraphrase the rest.\n"
    "4. Synthesise across sources into a unified answer; do not list them one by one.\n"
    "5. For interpretive questions give a grounded reading supported by lines.\n"
    "6. For factual questions be precise and cite directly.\n"
    "7. If the passages do not contain enough to answer, say so clearly.\n"
    "8. Keep answers concise: 3-6 sentences for simple questions, "
    "one short paragraph for interpretive ones."
)


def build_user_prompt(query, context_string):
    return (
        f"Question: {query}\n\n"
        f"Poem passages (cite these as [Source N]):\n"
        f"{context_string}\n\n"
        "Answer:"
    )


def call_openrouter(messages, model=None, api_key=None, temperature=0.3, max_tokens=512):
    key = api_key or OPENROUTER_API_KEY
    if not key:
        raise ValueError(
            "OPENROUTER_API_KEY is not set. "
            "Add it to Streamlit secrets or set the environment variable."
        )
    mdl = model or OPENROUTER_MODEL
    payload = json.dumps({
        "model": mdl,
        "messages": messages,
        "temperature": temperature,
        "max_tokens": max_tokens,
    }).encode("utf-8")
    req = urllib.request.Request(
        OPENROUTER_URL,
        data=payload,
        headers={
            "Authorization": f"Bearer {key}",
            "Content-Type":  "application/json",
            "HTTP-Referer":  "https://wasteland-rag.streamlit.app",
            "X-Title":       "Waste Land RAG",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = json.loads(resp.read().decode("utf-8"))
        return data["choices"][0]["message"]["content"].strip()
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"OpenRouter HTTP {e.code}: {body}") from e
    except Exception as e:
        raise RuntimeError(f"OpenRouter call failed: {e}") from e


def answer(query, k=4, api_key=None, model=None):
    results, context_string = retrieve_and_format(query, k=k)
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user",   "content": build_user_prompt(query, context_string)},
    ]
    llm_answer = call_openrouter(messages, api_key=api_key, model=model)
    return {
        "query":          query,
        "results":        results,
        "context_string": context_string,
        "answer":         llm_answer,
        "sources":        [r["stanza_label"] for r in results],
    }


if __name__ == "__main__":
    q = "What does the thunder say in the poem?"
    print(f"Query: {q}\n")
    try:
        out = answer(q, k=3)
        print("Answer:\n", out["answer"])
    except ValueError as e:
        print(f"[Skipped -- {e}]")
