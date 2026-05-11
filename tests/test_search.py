import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from search import find_pages


INDEX = {
    "hello": {
        "http://a.com": {"freq": 1, "positions": [0]},
        "http://b.com": {"freq": 1, "positions": [5]}
    },
    "world": {
        "http://a.com": {"freq": 1, "positions": [1]},
        "http://c.com": {"freq": 1, "positions": [2]}
    },
    "onlyb": {
        "http://b.com": {"freq": 1, "positions": [0]}
    }
}


class TestFindPages:
    def test_single_word_found(self):
        result = find_pages(INDEX, ["hello"])
        assert result == ["http://a.com", "http://b.com"]

    def test_single_word_not_found(self):
        result = find_pages(INDEX, ["nope"])
        assert result == []

    def test_multi_word_all_match(self):
        result = find_pages(INDEX, ["hello", "world"])
        assert result == ["http://a.com"]

    def test_multi_word_partial_match(self):
        result = find_pages(INDEX, ["hello", "onlyb"])
        assert result == ["http://b.com"]

    def test_multi_word_no_match(self):
        result = find_pages(INDEX, ["hello", "world", "onlyb"])
        assert result == []

    def test_empty_query(self):
        result = find_pages(INDEX, [])
        assert result == []


    def test_case_insensitive(self):
        result = find_pages(INDEX, ["HELLO", "World"])
        assert result == ["http://a.com"]
