"""streamlit_app.py — The Waste Land RAG assistant UI."""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import streamlit as st
import importlib

rag   = importlib.import_module("07_prompting")
store = importlib.import_module("05_create_chroma_store")

# Inject Streamlit secrets into rag module
try:
    if not rag.OPENROUTER_API_KEY:
        rag.OPENROUTER_API_KEY = st.secrets.get("OPENROUTER_API_KEY", "")
        rag.OPENROUTER_MODEL   = st.secrets.get("OPENROUTER_MODEL", rag.OPENROUTER_MODEL)
except Exception:
    pass

# Page config
st.set_page_config(
    page_title="The Waste Land -- RAG Assistant",
    page_icon="📖",
    layout="centered",
)

# Custom CSS
st.markdown("""
<style>
    h1 { color: #c9a84c; font-family: Georgia, serif; }
    h3 { color: #c9a84c; }
    .source-box {
        background-color: #1a1a1a;
        border-left: 3px solid #c9a84c;
        padding: 0.8rem 1rem;
        margin: 0.5rem 0;
        border-radius: 4px;
        font-family: Georgia, serif;
        font-size: 0.88rem;
        color: #d4d0c8;
        white-space: pre-wrap;
    }
    .answer-box {
        background-color: #111;
        border: 1px solid #c9a84c44;
        padding: 1rem 1.2rem;
        border-radius: 6px;
        font-family: Georgia, serif;
        font-size: 1rem;
        color: #e8e4d8;
        line-height: 1.7;
    }
    .stButton > button {
        background-color: #c9a84c;
        color: #0f0f0f;
        font-weight: bold;
        border-radius: 4px;
        border: none;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("# 📖 The Waste Land")
st.markdown("### T. S. Eliot — RAG Literary Assistant")
st.markdown("_Ask any question about the poem. Answers are grounded in poem text with cited sources._")
st.divider()


# Load ChromaDB (cached — built once per deployment)
@st.cache_resource(show_spinner="Building poem index — first run only, please wait...")
def load_collection():
    return store.get_or_build_collection()


collection = load_collection()

# Sidebar
with st.sidebar:
    st.markdown("## Settings")
    k = st.slider("Stanzas to retrieve (k)", min_value=1, max_value=6, value=4)
    show_sources = st.toggle("Show retrieved passages", value=True)
    show_scores  = st.toggle("Show similarity scores",  value=False)
    st.divider()
    st.markdown("## About")
    st.markdown(
        "*The Waste Land* (1922) is T. S. Eliot's landmark modernist poem "
        "in five sections. This assistant retrieves directly from poem text -- "
        "no external knowledge is used."
    )
    st.divider()
    st.markdown("## Example Questions")
    examples = [
        "What does the thunder say?",
        "Who is Tiresias and what is his role?",
        "What does water symbolize in the poem?",
        "Which section uses fragmentation most intensely?",
        "What happens in the pub scene?",
        "Who is Madame Sosostris?",
        "What is the significance of Shantih at the end?",
        "Describe the relationship between the typist and the clerk.",
    ]
    for eq in examples:
        if st.button(eq, key=f"ex_{eq}", use_container_width=True):
            st.session_state["prefill_query"] = eq

# Chat history
if "messages" not in st.session_state:
    st.session_state["messages"] = []

for msg in st.session_state["messages"]:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Input
prefill = st.session_state.pop("prefill_query", "")
query   = st.chat_input(placeholder="Ask about The Waste Land...") or prefill

# Process
if query:
    st.session_state["messages"].append({"role": "user", "content": query})
    with st.chat_message("user"):
        st.markdown(query)

    if not rag.OPENROUTER_API_KEY:
        st.error(
            "**API key not configured.**\n\n"
            "On Streamlit Cloud: add it under *Manage App > Secrets*.\n\n"
            "Locally: set OPENROUTER_API_KEY in `.streamlit/secrets.toml`."
        )
        st.stop()

    with st.chat_message("assistant"):
        with st.spinner("Retrieving passages and generating answer..."):
            try:
                out = rag.answer(query, k=k)
            except RuntimeError as e:
                st.error(f"Error from OpenRouter: {e}")
                st.stop()

        st.markdown(
            f'<div class="answer-box">{out["answer"]}</div>',
            unsafe_allow_html=True,
        )

        if show_sources and out["results"]:
            st.markdown("---")
            st.markdown("**Retrieved passages**")
            for i, r in enumerate(out["results"], 1):
                score_txt = f" &nbsp; score: {r['score']:.3f}" if show_scores else ""
                st.markdown(f"**[Source {i}]** {r['stanza_label']}{score_txt}", unsafe_allow_html=True)
                st.markdown(f'<div class="source-box">{r["text"]}</div>', unsafe_allow_html=True)

        st.session_state["messages"].append({"role": "assistant", "content": out["answer"]})

st.divider()
st.markdown(
    "<small>*The Waste Land* (1922) is in the public domain. "
    "Answers are grounded in poem text only.</small>",
    unsafe_allow_html=True,
)
