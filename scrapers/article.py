import requests
from bs4 import BeautifulSoup
from .settings import USER_AGENT

class Article():

    BASE_URL: str

    def __init__(self, base_url: str):
        self.BASE_URL = base_url
    
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