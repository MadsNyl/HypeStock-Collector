from collections import deque
from bs4 import BeautifulSoup, NavigableString, ResultSet

from app.crawler.scraper import scraper
from app.http.proxy import Proxy
from app.enums import HTML, Attribute


def crawl_articles(
    start_url: str,
    base_url: str,
    newspaper: str,
    tickers: list[str],
    visited_urls: list[str],
    proxy: Proxy,
    cap: int = 10
):
    visited = set()
    queue = deque()

    visited.add(start_url)
    queue.append(start_url)

    while queue and len(visited) < cap:
        url_node = queue.popleft()
        html_page: BeautifulSoup = scraper.html(url_node, proxy.proxy)

        urls: list[str] = []

        if html_page:
            urls = extract_hrefs(html_page)
            print(urls)


def extract_hrefs(html_page: BeautifulSoup) -> list[str]:
    anchor_tags = html_page.find_all(HTML.ANCHOR.value, href=True)
    return list(map(lambda x: x[Attribute.HREF.value], anchor_tags))