import requests
from bs4 import BeautifulSoup
from db import API
from ..settings import USER_AGENT
from util import is_string_valid, get_stock_data, emoji_free_text

class Article():

    BASE_URL: str
    STOCK_SYMBOLS: list[str]
    STOCK_NAMES: list[str]

    def __init__(self, base_url: str):
        self.BASE_URL = base_url
        self.__get_stock_info()
    
    def __get_stock_info(self) -> None:
        stock_info = API.get_stock_info()
        self.STOCK_SYMBOLS = [i[0] for i in stock_info]
        self.STOCK_NAMES = [i[1] for i in stock_info]
        
    def _get_html(self, url: str) -> str:
        try:
            res = requests.get(url)
            if res.status_code != 200:
                headers = {"User-Agent": USER_AGENT}
                res = requests.get(url, headers=headers)
                if res.status_code != 200: return None
            return BeautifulSoup(res.text, "html.parser")
        except Exception as e:
            raise Exception(e)
    
    def _strip_url(self, url: str) -> str: return url.split("/")[-1] 

    def __strip_text(self, text: str) -> str: return list(filter(lambda x: len(x), text.strip().replace("(", " ").replace(")", " ").split(" ")))

    def __analyze_text(self, text: list[str]) -> list[dict]:
        hits = []
        for word in text:
            if word in [i["ticker"] for i in hits]: continue

            if self.__is_db_match(word):
                hits.append({
                    "ticker": word,
                    "new": False
                })
                continue

            if is_string_valid(word):
                hits.append({
                    "ticker": word,
                    "new": True
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
        for hit in hits:

            if hit["ticker"] in self.STOCK_SYMBOLS:
                results.append(hit)
                continue

            name, exchange = get_stock_data(hit["ticker"])
            if name is not None and exchange is not None: results.append(hit)
        
        return results

    def __is_db_match(self, word: str) -> bool: return word in self.STOCK_NAMES or word in self.STOCK_SYMBOLS

    def _insert_stock(self, stock: str) -> None:
        name, exchange = get_stock_data(stock)
        API.insert_stock(stock, name, exchange)

    def _insert_article(self, provider: str, external: bool, body: str, title: str, url: str, created_date: str) -> int:
        return API.insert_article(provider, external, title, url, body, created_date)
    
    def _insert_article_stock(self, symbol: str, article_id: int) -> None:
        API.insert_article_stock(symbol, article_id)