import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

import pytest
from unittest.mock import patch, Mock
from bs4 import BeautifulSoup
from crawler import get_page, crawl_site


# --- sample HTML that mimics quotes.toscrape.com ---
PAGE1_HTML = """
<html><body>
<div class="quote"><span class="text">"Hello world"</span></div>
<li class="next"><a href="/page/2/">Next &rarr;</a></li>
</body></html>
"""

PAGE2_HTML = """
<html><body>
<div class="quote"><span class="text">"Goodbye world"</span></div>
</body></html>
"""


def make_response(html, status=200):
    r = Mock()
    r.status_code = status
    r.text = html
    return r


# test for craw page
class TestGetPage:
    def test_returns_soup_on_200(self):
        with patch('crawler.requests.get') as mock_get:
            mock_get.return_value = make_response(PAGE1_HTML)
            soup = get_page('http://test.com')
            assert soup is not None
            assert soup.find('li', class_='next') is not None

    def test_returns_none_on_error(self):
        with patch('crawler.requests.get') as mock_get:
            mock_get.return_value = make_response('', status=404)
            soup = get_page('http://test.com')
            assert soup is None

    def test_returns_none_on_exception(self):
        with patch('crawler.requests.get') as mock_get:
            import requests
            mock_get.side_effect = requests.ConnectionError('network error')
            soup = get_page('http://test.com')
            assert soup is None


# test for craw site
class TestCrawlSite:
    def test_crawls_all_pages(self):
        with patch('crawler.get_page') as mock_get_page:
            soup1 = BeautifulSoup(PAGE1_HTML, 'html.parser')
            soup2 = BeautifulSoup(PAGE2_HTML, 'html.parser')
            mock_get_page.side_effect = [soup1, soup2]

            with patch('crawler.time.sleep'):
                pages = crawl_site('http://test.com/page/1/', delay=0)

            assert len(pages) == 2
            assert 'http://test.com/page/1/' in pages
            assert 'http://test.com/page/2/' in pages

    def test_stops_on_broken_page(self):
        with patch('crawler.get_page') as mock_get_page:
            mock_get_page.return_value = None

            with patch('crawler.time.sleep'):
                pages = crawl_site('http://test.com/', delay=0)

            assert len(pages) == 0
