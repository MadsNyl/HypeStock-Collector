from bs4 import BeautifulSoup

from app.http import http
from app.enums import HttpKwargs, Parser
from settings import USER_AGENT


class Scraper():
    
    def html(self, url: str, proxy: str) -> BeautifulSoup:
        try:
            headers = {
                HttpKwargs.USER_AGENT.value: USER_AGENT
            }
            proxies = {
                HttpKwargs.HTTP.value: f"http://{proxy}"
            }

            response = http.get(url=url, headers=headers, timeout=2, proxies=proxies)
            return BeautifulSoup(response.text, Parser.HTML.value)
        except Exception as e:
            print(f"Fetching html error: {e}")


scraper = Scraper()