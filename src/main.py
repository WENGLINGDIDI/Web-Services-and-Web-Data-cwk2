import json
import sys

from crawler import crawl_site
from indexer import build_index, save_index, load_index
from search import find_pages

BASE_URL = 'https://quotes.toscrape.com/'
INDEX_PATH = 'data/index.json'

index = None  # current in-memory index


def cmd_build():
    global index
    print("Building index...")
    pages = crawl_site(BASE_URL, delay=6)
    index = build_index(pages)
    save_index(index, INDEX_PATH)
    print("Build complete.")


def cmd_load():
    global index
    index = load_index(INDEX_PATH)
    if index is not None:
        print("Load complete.")


def cmd_print(word):
    global index
    w = word.lower()
    if w in index:
        print(json.dumps(index[w], indent=2))
    else:
        print(f"'{word}' not found.")


def cmd_find(words):
    global index
    results = find_pages(index, words)
    if results:
        for url in results:
            print(url)
    else:
        print("No matching pages.")


def main():
    global index
    print("Input Commands: build | load | print <word> | find <words> | quit")

    while True:
        try:
            line = input("> ").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            break

        if not line:
            continue

        parts = line.split()
        cmd = parts[0].lower()

        if cmd == 'quit' or cmd == 'exit':
            break
        elif cmd == 'build':
            cmd_build()
        elif cmd == 'load':
            cmd_load()
        elif cmd == 'print':
            if index is None:
                cmd_load()
            if index and len(parts) >= 2:
                cmd_print(parts[1])
            elif not index:
                print("No index loaded. Run build or load first.")
        elif cmd == 'find':
            if index is None:
                cmd_load()
            if index and len(parts) >= 2:
                cmd_find(parts[1:])
            elif not index:
                print("No index loaded. Run build or load first.")
        else:
            print(f"Unknown: {cmd}")


if __name__ == '__main__':
    main()
