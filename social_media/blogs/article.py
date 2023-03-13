import requests
from bs4 import BeautifulSoup
from db import INSERT, GET
from ..settings import USER_AGENT
from util import is_string_valid, get_stock_data, emoji_free_text

class Article():

    BASE_URL: str
    STOCK_SYMBOLS: list[str]
    STOCK_NAMES: list[str]

    def __init__(self, base_url: str):
        self.BASE_URL = base_url
        self._get_stock_info()
    
    def _get_stock_info(self) -> None:
        stock_info = GET.stock_info()
        self.STOCK_SYMBOLS = dict.fromkeys([i[0] for i in stock_info])
        self.STOCK_NAMES = [i[1] for i in stock_info]
        
    def _get_html(self, url: str) -> str:
        try:
            res = requests.get(url, timeout=2)
            if res.status_code != 200:
                headers = {"User-Agent": USER_AGENT}
                res = requests.get(url, headers=headers)
                if res.status_code != 200: return None
            return BeautifulSoup(res.text, "html.parser")
        except Exception as e:
            headers = {"User-Agent": USER_AGENT}
            res = requests.get(url, headers=headers)
            return BeautifulSoup(res.text, "html.parser")
    
    def _strip_url(self, url: str) -> str: return url.split("/")[-1] 

    def __strip_text(self, text: str) -> str: return list(filter(lambda x: len(x), text.strip().replace("(", " ").replace(")", " ").split(" ")))

    def __analyze_text(self, text: list[str]) -> list[dict]:
        hits = []

        # if self.__is_name_match(text.lower()) is not None: 
        #     if 

        for word in text:
            if word in [i["ticker"] for i in hits]: continue

            if word in self.STOCK_SYMBOLS:
                hits.append({
                    "ticker": word,
                    "new": False
                })
                continue
    
        return hits
    
    def _strip_emojies(self, text: str) -> str: return emoji_free_text(text)     

    def _process_text_body(self, text: str) -> list[dict]:
        body = emoji_free_text(text)
        body = self.__strip_text(text)
        hits = self.__analyze_text(body)
        return self.__parsed_hits(hits)
        
    def __parsed_hits(self, hits: list[dict]) -> list[dict]:
        results = []
        for hit in hits: results.append(hit)
        
        return results

    def __is_db_match(self, word: str) -> bool: return word in self.STOCK_SYMBOLS

    def __is_name_match(self, words: list[str]) -> bool:
        for name in self.STOCK_SYMBOLS:
            if name.lower() in words: return name
        return None
    
    def _is_url_match(self, url: str) -> bool: return GET.article_url(url) is not None

    def _insert_stock(self, stock: str) -> None:
        name, exchange = get_stock_data(stock)
        INSERT.stock(stock, name, exchange)

    def _insert_article(self, provider: str, external: bool, body: str, title: str, url: str, created_date: str) -> int: return INSERT.article(provider, external, title, url, body, created_date)

    def _insert_external_article(self, provider: str, external: bool, body: str, title: str, url: str, created_date: str) -> int: return INSERT.article(provider, external, title, url, body, created_date)
    
    def _insert_article_stock(self, symbol: str, article_id: int) -> None: INSERT.article_stock(symbol, article_id)