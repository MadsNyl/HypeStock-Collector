from .article import Article
from util import progressbar

class Yahoo(Article):

    __ARTICLE_CLASS: str = "js-stream-content Pos(r)"
    __YAHOO_URL: str =  "https://finance.yahoo.com"
    __PROVIDER: str = "yahoo finance"

    def __init__(self, base_url):
        super().__init__(base_url)

    def run(self):
        articles = self.__get_all_articles()
        progressbar(0, len(articles), f"Processing {len(articles)} articles:")
        for i, article in enumerate(articles): 
            self.__process_article(article)
            progressbar(i + 1, len(articles), None) 

    def __process_article(self, article: object) -> None:
            tag = article.find("a", href=True)
            url = self.__format_url(tag["href"])

            if super()._is_url_match(url): return

            body = super()._get_html(url)
            if not body: return

            external_url = self.__is_external_article(body)

            title = tag.text

            text_body = self._get_text_body(body)

            datetime = body.find("time")

            if external_url: text_body = self.__process_external_article(text_body)
            text_body = super()._strip_emojies(text_body)
            hits = super()._process_text_body(text_body)

            if not len(hits): return

            article_id = super()._insert_article(self.__PROVIDER, False, text_body, title, url, datetime)

            for hit in hits:
                if hit["new"]: super()._insert_stock(hit["ticker"])
                super()._insert_article_stock(hit["ticker"], article_id)
    
    def _get_text_body(body: object) -> str: body.find("div", class_="caas-body").text

    def __process_external_article(self, text: str) -> str: return text.replace("continue reading", "") 

    def __is_external_article(self, body: object) -> str:
        continue_button = body.find(lambda a: a.name == "a" and a.text.lower() == "continue reading")
        if continue_button: return continue_button["href"]
        return None

    def __format_url(self, url: str) -> str: return self.__YAHOO_URL + url.replace(self.__YAHOO_URL, "") 

    def __get_all_articles(self) -> list:
        try:
            body = super()._get_html(self.BASE_URL)
            return body.find_all("li", class_=self.__ARTICLE_CLASS)
        except Exception as e:
            raise Exception(e)
    