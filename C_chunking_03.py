"""03_chunking.py — Stanza-level chunks with annotation-enriched search_text."""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import importlib
preprocessing = importlib.import_module("02_preprocessing")
get_preprocessed_stanzas = preprocessing.get_preprocessed_stanzas

ANNOTATIONS = {
    "sec1_stanza0": "spring memory desire rebirth seasonal cycle April cruelest",
    "sec1_stanza1": "winter forgetfulness snow shelter dormancy",
    "sec1_stanza2": "Starnbergersee Bavaria pre-war Europe aristocracy leisure memory",
    "sec1_stanza3": "Marie Germany childhood sled freedom winter multilingual",
    "sec1_stanza4": "desert wasteland broken images fear dust water absence Ezekiel Bible",
    "sec1_stanza5": "hyacinth garden love silence paralysis Wagner Tristan Isolde German",
    "sec1_stanza6": "Madame Sosostris Tarot cards drowned Phoenician Sailor fortune death",
    "sec1_stanza7": "Unreal City London Bridge crowd death urban Dante fog winter",
    "sec1_stanza8": "Stetson Mylae war corpse garden burial Baudelaire reader",
    "sec2_stanza0": "burnished throne opulence Cleopatra Shakespeare Antony women",
    "sec2_stanza1": "perfumes synthetic sensory artifice excess",
    "sec2_stanza2": "Philomel nightingale rape Tereus myth Ovid Jug Jug violated beauty",
    "sec2_stanza3": "withered stumps anxiety footsteps silence",
    "sec2_stanza4": "nerves speak communication breakdown marriage loveless relationship",
    "sec2_stanza5": "rats alley dead men bones war decay",
    "sec2_stanza6": "nothing wind silence emptiness existential",
    "sec2_stanza7": "Shakespeare Tempest pearls Shakespeherian Rag fragmentation jazz",
    "sec2_stanza8": "pub Lil Albert demob working class marriage post-war",
    "sec2_stanza9": "Ophelia goodnight pub farewell",
    "sec3_stanza0": "Thames nymphs departed river pastoral elegy Spenser pollution",
    "sec3_stanza1": "Leman exile Psalm 137 Babylon lamentation weeping bones",
    "sec3_stanza2": "rat fishing canal gashouse Fisher King bones decay Marvell",
    "sec3_stanza3": "Mrs Porter Sweeney spring French voices Verlaine",
    "sec3_stanza4": "nightingale Philomel Jug Jug bird song fragmented",
    "sec3_stanza5": "Unreal City Smyrna merchant Eugenides commerce",
    "sec3_stanza6": "Tiresias blind prophet seer androgyne two lives violet hour typist",
    "sec3_stanza7": "Tiresias typist laundry divan foresuffering prophecy",
    "sec3_stanza8": "carbuncular clerk typist class seduction joyless loveless",
    "sec3_stanza9": "Tiresias Thebes foresuffered indifference vanity",
    "sec3_stanza10": "gramophone automatic mechanical indifference loveless woman folly",
    "sec3_stanza11": "Magnus Martyr church music beauty Thames Ionian",
    "sec3_stanza12": "Thames river barges tide Rhine maidens Wagner industrial",
    "sec3_stanza13": "Elizabeth Leicester Tudor history river pageant past",
    "sec3_stanza14": "Margate Sands fragmentation nothing connect Thames daughter broken",
    "sec3_stanza15": "Buddha Fire Sermon Carthage burning Augustine desire spiritual",
    "sec4_stanza0": "Phlebas Phoenician drowned dead water sea death bones whirlpool",
    "sec4_stanza1": "Consider Phlebas warning mortal Gentile Jew wheel",
    "sec5_stanza0": "agony death dying living Christ resurrection patience garden",
    "sec5_stanza1": "no water rock desert thirst drought Grail wasteland spiritual",
    "sec5_stanza2": "third figure road Emmaus stranger hooded hallucinatory",
    "sec5_stanza3": "falling towers Jerusalem Athens Alexandria Vienna London apocalypse",
    "sec5_stanza4": "bats towers bells nightmare surreal exhausted wells",
    "sec5_stanza5": "empty chapel Grail dry bones cock crow rain renewal",
    "sec5_stanza6": "thunder DA Datta give Dayadhvam sympathise Damyata control Upanishads Sanskrit",
    "sec5_stanza7": "fragments shored ruins Shantih peace London Bridge Fisher King Hieronymo",
}


def get_chunks():
    chunks = []
    for s in get_preprocessed_stanzas():
        ann = ANNOTATIONS.get(s["stanza_id"], "")
        chunks.append({
            "chunk_id":       s["stanza_id"],
            "section_number": s["section_number"],
            "section_title":  s["section_title"],
            "stanza_index":   s["stanza_index"],
            "stanza_label":   (
                f"Section {s['section_number']} "
                f"({s['section_title']}), "
                f"Stanza {s['stanza_index'] + 1}"
            ),
            "first_line":     s["first_line"],
            "text":           s["text"],
            "search_text":    f"{s['section_title']} {s['text']} {ann}",
        })
    return chunks


if __name__ == "__main__":
    chunks = get_chunks()
    print(f"Total chunks: {len(chunks)}")
