from .article import Article
import requests

class CNBC(Article):

    __CNBC_URL: str =  "https://finance.yahoo.com"

    def __init__(self, base_url):
        super().__init__(base_url)
    
    def run(self):
        articles = self.__get_all_articles()
        for article in articles: self.__process_article(article)

    def __get_all_articles(self) -> list:
        try:
            body = super()._get_html(self.BASE_URL)
            content_wrapper = body.find("div", class_="SectionWrapper-content")
        except Exception as e:
            raise Exception(e)