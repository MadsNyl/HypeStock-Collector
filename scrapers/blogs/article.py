import requests
from bs4 import BeautifulSoup
from db import API
from ..settings import USER_AGENT
from util import is_string_valid, get_stock_data

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
            if self.__is_db_match(word) and word not in hits:
                hits.append({
                    "ticker": word,
                    "new": False
                })
                continue

            if is_string_valid(word) and word not in hits:
                hits.append({
                    "ticker": word,
                    "new": True
                })
                continue
        
        return hits
    
    def _process_text_body(self, text: str) -> list[dict]:
        body = self.__strip_text(text)
        return self.__analyze_text(body)
        
    def __is_db_match(self, word: str) -> bool: return word in self.STOCK_NAMES or word in self.STOCK_SYMBOLS

    def _insert_stock(self, stock: str) -> None:
        name, exchange = get_stock_data(stock)
        API.insert_stock(stock, name, exchange)

    def _insert_article(self, stock: str, body: str, title: str) -> None:
        pass