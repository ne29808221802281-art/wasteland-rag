"""02_preprocessing.py — Clean and normalise stanza text."""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import importlib
documents = importlib.import_module("01_documents")
get_all_sections = documents.get_all_sections


def clean_stanza(text):
    replacements = {
        "\u2018": "'", "\u2019": "'",
        "\u201c": '"', "\u201d": '"',
        "\u2014": "--", "\u2013": "-",
        "\u2026": "...",
    }
    for char, rep in replacements.items():
        text = text.replace(char, rep)
    lines = [line.rstrip() for line in text.split("\n")]
    cleaned, prev_blank = [], False
    for line in lines:
        is_blank = line.strip() == ""
        if is_blank and prev_blank:
            continue
        cleaned.append(line)
        prev_blank = is_blank
    return "\n".join(cleaned).strip()


def get_preprocessed_stanzas():
    records = []
    for sec in get_all_sections():
        for idx, raw in enumerate(sec["stanzas"]):
            cleaned = clean_stanza(raw)
            first_line = next(
                (l.strip() for l in cleaned.split("\n") if l.strip()), ""
            )
            records.append({
                "stanza_id":      f"sec{sec['section_number']}_stanza{idx}",
                "section_number": sec["section_number"],
                "section_title":  sec["section_title"],
                "stanza_index":   idx,
                "first_line":     first_line,
                "text":           cleaned,
            })
    return records


if __name__ == "__main__":
    stanzas = get_preprocessed_stanzas()
    print(f"Preprocessed stanzas: {len(stanzas)}")
