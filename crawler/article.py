from db import API
from social_media import Article
from bs4 import BeautifulSoup
from datetime import datetime
from .scraper import ArticleScraper
import re

class ArticleCrawler(Article):

    scraper: ArticleScraper = ArticleScraper()
    URLS: list[str]

    def __init__(self, urls: list[str]):
        super()._get_stock_info()
        self.URLS = urls
    
    def run(self) -> None:
        for url in self.URLS:
            print(f"Crawling {url}")
            self._crawl_page(url)

    def _crawl_page(self, url: str) -> None:
        anchors = self._get_anchor_tags(url)
        anchors = self._filter_links(anchors)
        anchors = self._add_base_urls(anchors, url)
        for article in anchors: self._crawl_article(article)
    
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
            case _:
                data = None

        self._handle_data(data)
    
    def _handle_data(self, data: dict) -> None:
        if data is None: return
        if not len(data["hits"]): return
        if super()._is_url_match(data["url"]): return

        article_id = super()._insert_article(
            data["provider"],
            False,
            data["text_body"],
            data["title"],
            data["url"],
            data["datetime"]
        )

        for hit in data["hits"]:
            if hit["new"]: super()._insert_stock(hit["ticker"])
            super()._insert_article_stock(hit["ticker"], article_id)


    def _handle_yahoo(self, url: str) -> dict:
        body = super()._get_html(url)
        text_body = super()._strip_emojies(body.find("div", class_="caas-body").text)
        return {
            "url": url,
            "provider": "yahoo finance",
            "title": body.find("div", class_="caas-title-wrapper").find("h1").text,
            "text_body": text_body,
            "hits": super()._process_text_body(text_body),
            "datetime": body.find("time")["datetime"][:-5]
        }
    
    def _handle_cnbc(self, url: str) -> dict:
        body = super()._get_html(url)
        try:
            text_body = super()._strip_emojies(body.find("div", class_="ArticleBody-articleBody").text)
            return {
                "url": url,
                "provider": "cnbc",
                "title": body.find("h1", class_="ArticleHeader-headline").text,
                "text_body": text_body,
                "hits": super()._process_text_body(text_body),
                "datetime": body.find("time")["datetime"][:-5]
            }
        except Exception as e:
            print(url)
            return None
    
    def _handle_cnn(self, url: str) -> dict:
        body = super()._get_html(url)
        try: 
            text_body = super()._strip_emojies(body.find("div", class_="article__content-container").text).strip()
            date_text = body.find("div", class_="timestamp").text.replace("Updated", "").replace("Published", "").strip()
            date = f"{date_text[17:20]} {date_text[23:25]} {date_text[27:31]}"
            date = datetime.strptime(date, "%b %d %Y").date()
            return {
                "url": url,
                "provider": "cnn",
                "title": body.find("h1", class_="headline__text").text,
                "text_body": text_body,
                "hits": super()._process_text_body(text_body),
                "datetime": date
            }
        except Exception as e:
            print(e)
            print(url)

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

    def _filter_links(self, urls) -> list[str]: 
        html = self._filter_news(urls)
        date = self._filter_links_date(urls)
        article = self._filter_links_article(urls)
        return list(set(html + date + article))

    def _filter_links_date(self, urls) -> list[str]: return list(filter(lambda x: re.compile(r"/([0-9]+(/[0-9]+)+)/", re.IGNORECASE).match(x), urls)) 
