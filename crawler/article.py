from db import API
from social_media import Article
from bs4 import BeautifulSoup

class ArticleCrawler(Article):

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
        anchors = self._filter_news(anchors)
        anchors = self._add_base_urls(anchors, url)
        for article in anchors: self._crawl_article(article)
    
    def _crawl_article(self, url: str) -> None:
        state = self._get_base_url(url)
        
        match state:
            case "finance.yahoo.com":
                data = self._handle_yahoo(url)
            case "www.cnbc.com":
                data = self._handle_cnbc(url)
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
    
    def _handle_cnbc(self, url: str) -> None:
        print(f"CNBC: {url}")

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
    
    def _filter_news(self, urls, tag=".html") -> str: return list(filter(lambda x: x.endswith(tag), urls))

    def _filter_links(self, urls, tag) -> str: return list(filter(lambda x: x.startswith(tag), urls))     
