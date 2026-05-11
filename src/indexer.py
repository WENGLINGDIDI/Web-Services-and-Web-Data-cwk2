import json
import re
import os


def tokenize(text):
    return re.findall(r'[a-z0-9]+', text.lower())


def build_index(pages):
    index = {}

    for url, text in pages.items():
        words = tokenize(text)
        # group positions for each word on this page
        page_words = {}
        for pos, w in enumerate(words):
            if w not in page_words:
                page_words[w] = []
            page_words[w].append(pos)
        # merge into global index
        for w, positions in page_words.items():
            if w not in index:
                index[w] = {}
            index[w][url] = {
                'freq': len(positions),
                'positions': positions
            }
    return index


def save_index(index, filepath):
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(index, f, indent=2, ensure_ascii=False)
    print(f"Index saved to {filepath} ({len(index)} words)")


def load_index(filepath):
    if not os.path.exists(filepath):
        print(f"Index file not found: {filepath}")
        return None
    with open(filepath, 'r', encoding='utf-8') as f:
        index = json.load(f)
    print(f"Index loaded from {filepath} ({len(index)} words)")
    return index
