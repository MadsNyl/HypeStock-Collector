from collections import deque
from bs4 import BeautifulSoup

from app.crawler.scraper import scraper
from app.http.proxy import Proxy
from app.enums import HTML, Attribute
from app.classes import Newspaper
from app.crawler.validator import ArticleValidator
from app.http import http, Proxy, build_url, parse_object
from settings import API_URL



def crawl_articles(newspaper: Newspaper, cap: int = 10):
    visited_urls = set()
    queue = deque()

    old_urls_response = http.get(
        build_url(
                f"{API_URL}article",
                [
                    "url_only=true",
                    f"newspaperId={newspaper.id}"
                ]
            )
    )

    old_urls = [
        parse_object(object, "url")
        for object in old_urls_response.json()
    ]

    proxy = Proxy

    visited_urls.add(newspaper.start_url)
    queue.append(newspaper.start_url)

    while queue and len(visited_urls) < cap:
        url_node = queue.popleft()
        html_page: BeautifulSoup = scraper.html(url_node, proxy.proxy)

        urls: list[str] = []

        if html_page:
            urls = extract_hrefs(html_page)
        
        for url in urls:
            validator = ArticleValidator(url, newspaper.provider)

            if validator.is_sliced_url:
                url = validator.build_url(newspaper.base_url)

            if (
                validator.is_social_media_url or
                url in visited_urls or
                url in  old_urls
            ):
                continue
            
            if validator.is_valid:
                visited_urls.add(url)
                queue.append(url)
                old_urls.append(url)
        
        visited_urls.discard(newspaper.start_url)
        return visited_urls
    

def extract_hrefs(html_page: BeautifulSoup) -> list[str]:
    anchor_tags = html_page.find_all(HTML.ANCHOR.value, href=True)
    return list(map(lambda x: x[Attribute.HREF.value], anchor_tags))