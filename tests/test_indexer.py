import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

import json
import tempfile
from indexer import tokenize, build_index, save_index, load_index


class TestTokenize:
    def test_lowercase(self):
        assert tokenize("Hello WORLD") == ["hello", "world"]

    def test_removes_punctuation(self):
        assert tokenize("hello, world!") == ["hello", "world"]

    def test_keeps_numbers(self):
        assert tokenize("page2 test123") == ["page2", "test123"]

    def test_empty_string(self):
        assert tokenize("") == []

    def test_numbers_only(self):
        assert tokenize("123 456") == ["123", "456"]


class TestBuildIndex:
    def test_basic_index(self):
        pages = {
            "http://a.com": "hello world hello"
        }
        idx = build_index(pages)
        assert "hello" in idx
        assert "world" in idx
        assert idx["hello"]["http://a.com"]["freq"] == 2
        assert idx["hello"]["http://a.com"]["positions"] == [0, 2]
        assert idx["world"]["http://a.com"]["freq"] == 1
        assert idx["world"]["http://a.com"]["positions"] == [1]

    def test_multiple_pages(self):
        pages = {
            "http://a.com": "hello world",
            "http://b.com": "hello there"
        }
        idx = build_index(pages)
        assert len(idx["hello"]) == 2
        assert "http://a.com" in idx["hello"]
        assert "http://b.com" in idx["hello"]

    def test_case_insensitive(self):
        pages = {"http://a.com": "Hello HELLO hello"}
        idx = build_index(pages)
        assert idx["hello"]["http://a.com"]["freq"] == 3

    def test_empty_pages(self):
        idx = build_index({})
        assert idx == {}

    def test_no_text_pages(self):
        pages = {"http://a.com": ""}
        idx = build_index(pages)
        assert idx == {}


class TestSaveLoad:
    def test_roundtrip(self):
        index = {
            "hello": {
                "http://a.com": {"freq": 1, "positions": [0]}
            }
        }
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json',
                                         delete=False, encoding='utf-8') as f:
            f.write('')
            tmp = f.name

        try:
            save_index(index, tmp)
            loaded = load_index(tmp)
            assert loaded == index
        finally:
            os.remove(tmp)

    def test_load_nonexistent(self):
        result = load_index('/no/such/path/index.json')
        assert result is None
