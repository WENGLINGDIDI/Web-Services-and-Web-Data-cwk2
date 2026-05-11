# Search Engine Tool

A simple search engine for the website quotes.toscrape.com. It crawls all pages, builds an inverted index, and lets you search for words from the command line. Built for COMP/XJCO 3011 Coursework 2.

## Dependencies

- Python 3.x
- requests
- beautifulsoup4
- pytest (for testing)

## Setup

```bash
pip install -r requirements.txt
```

## Usage

Run the program:

```bash
python src/main.py
```

You will see a prompt `>` where you can type these commands:

### build

Crawl the website, create the inverted index, and save it to a file.

```
> build
```

This takes about a minute because there is a 6-second wait between requests.

### load

Load a previously saved index from the file system.

```
> load
```

### print

Show the index entry for a word (which pages it appears in, how many times, and at what positions).

```
> print nonsense
> print life
```

If the word is not in the index, it will say so.

### find

Search for pages that contain **all** of the given words.

```
> find indifference
> find good friends
> find the world
```

If no pages match, it prints "No matching pages."

### quit

Exit the program.

```
> quit
```

## Testing

```bash
pytest tests/ -v
```

This runs 24 tests covering the crawler, indexer, and search logic, including edge cases like empty input, missing words, and network errors.

## Project Structure

```
src/
  crawler.py    - crawls quotes.toscrape.com with 6s politeness window
  indexer.py    - builds, saves, and loads the inverted index
  search.py     - searches the index (AND logic for multi-word queries)
  main.py       - command-line interface
tests/
  test_crawler.py - 5 tests
  test_indexer.py - 10 tests
  test_search.py  - 7 tests
data/
  index.json    - the saved index (created after running build)
```
