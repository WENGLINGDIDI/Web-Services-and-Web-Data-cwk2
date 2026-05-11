import requests
from bs4 import BeautifulSoup
import time
from urllib.parse import urljoin


def get_page(url):
    try:
        resp = requests.get(url, timeout=10)
        if resp.status_code == 200:
            return BeautifulSoup(resp.text, 'html.parser')
        else:
            print(f"  Error fetching {url}: status {resp.status_code}")
            return None
    except requests.RequestException as e:
        print(f"  Error fetching {url}: {e}")
        return None

# Crawl quotes website starting from start_url.
def crawl_site(start_url, delay=6):
    pages = {}
    current_url = start_url

    while current_url:
        print(f"Crawling: {current_url}")
        soup = get_page(current_url)

        if soup is None:
            break

        # extract visible text from this page
        text = soup.get_text()
        pages[current_url] = text

        # find next page link
        next_li = soup.find('li', class_='next')
        if next_li and next_li.find('a'):
            next_href = next_li.find('a')['href']
            current_url = urljoin(start_url, next_href)
        else:
            current_url = None

        # politeness window
        if current_url is not None:
            print(f"  Waiting {delay}s (politeness)...")
            time.sleep(delay)

    print(f"Done: crawled {len(pages)} pages.")
    return pages


if __name__ == '__main__':
    pages = crawl_site('https://quotes.toscrape.com/')
    for url in pages:
        print(f"  {url}: {len(pages[url])} chars")
