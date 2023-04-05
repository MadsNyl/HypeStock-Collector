from db import GET
from social_media import Article
from .scraper import ArticleScraper
from util import progressbar
import re

class ArticleCrawler(Article):

    scraper: ArticleScraper = ArticleScraper()
    URLS: list[str]
    article_urls: dict[str: None]

    def __init__(self, urls: list[str]):
        super()._get_stock_info()
        self.URLS = urls
        self.article_urls = GET.article_urls()
    
    def run(self) -> None:
        for url in self.URLS: self._crawl_page(url)

    def _crawl_page(self, url: str) -> None:
        anchors = self._get_anchor_tags(url)
        anchors = self._filter_links(anchors)
        anchors = self._add_base_urls(anchors, url)

        progressbar(0, len(anchors), f"\nCrawling {len(anchors)} articles from {url}: ")
        for i, article in enumerate(anchors): 
            self._crawl_article(article)
            progressbar(i + 1, len(anchors), None)
    
    def _crawl_article(self, url: str) -> None:
        state = self._get_base_url(url)

        match state:
            case "finance.yahoo.com":
                data = self.scraper.yahoo(url) 
            case "www.cnbc.com":
                data = self.scraper.cnbc(url)
            case "edition.cnn.com":
                data = self.scraper.cnn(url)
            case "www.nasdaq.com":
                data = self.scraper.nasdaq(url)
            case "www.ft.com":
                data = self.scraper.ft(url)
            case _:
                data = None

        self._handle_data(data)
    
    def _handle_data(self, data: dict) -> None:
        if data is None: return
        if not len(data["hits"]): return
        if data["url"] in self.article_urls: return

        article_id = super()._insert_article(
            data["provider"],
            False,
            data["text_body"],
            data["title"],
            data["url"],
            data["datetime"]
        )

        for hit in data["hits"]:
            # if hit["new"]: super()._insert_stock(hit["ticker"])
            super()._insert_article_stock(hit["ticker"], article_id)

    def _get_anchor_tags(self, url: str) -> list[str]:
        base_page = super()._get_html(url)
        anchors = base_page.find_all("a", href=True)
        return list(map(lambda x: x["href"], anchors))

    def _add_base_urls(self, urls: list[str], base_url: str) -> list[str]:
        for i, url in enumerate(urls): 
            if url.startswith("/"): 
                urls[i] = f"{self._add_base_url(base_url)}{url}"
        return urls

    def _get_base_url(self, url: str) -> str: return url.replace('https://', '').split('/')[0]

    def _add_base_url(self, url: str) -> str: return f"https://{self._get_base_url(url)}"
    
    def _filter_news(self, urls: list[str], tag=".html") -> list[str]: return list(filter(lambda x: x.endswith(tag), urls))

    def _filter_links_article(self, urls: list[str]) -> list[str]: return list(filter(lambda x: "/articles/" in x, urls))

    def _filter_links_content(self, urls: list[str]) -> list[str]: return list(filter(lambda x: "/content/" in x, urls))

    def _filter_links(self, urls) -> list[str]: 
        html = self._filter_news(urls)
        date = self._filter_links_date(urls)
        article = self._filter_links_article(urls)
        content = self._filter_links_content(urls)
        return list(set(html + date + article + content))

    def _filter_links_date(self, urls) -> list[str]: return list(filter(lambda x: re.compile(r"/([0-9]+(/[0-9]+)+)/", re.IGNORECASE).match(x), urls)) 
