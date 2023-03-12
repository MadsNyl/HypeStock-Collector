from social_media import Article
from datetime import datetime

class ArticleScraper(Article):

    def __init__(self):
        super()._get_stock_info()

    def yahoo(self, url: str) -> dict:
        body = super()._get_html(url)
        try:
            text_body = super()._strip_emojies(body.find("div", class_="caas-body").text)
            return {
                "url": url,
                "provider": "yahoo finance",
                "title": body.find("div", class_="caas-title-wrapper").find("h1").text,
                "text_body": text_body,
                "hits": super()._process_text_body(text_body),
                "datetime": body.find("time")["datetime"][:-5]
            }
        except Exception as e:
            print(e)
            print(url)
            return None

    def cnbc(self, url: str) -> dict:
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
    
    def cnn(self, url: str) -> dict:
        body = super()._get_html(url)
        try: 
            text_body = super()._strip_emojies(body.find("div", class_="article__content-container").text).strip()
            date_text = body.find("div", class_="timestamp").text.replace("Updated", "").replace("Published", "").replace(",", "").strip()
            date = date_text.split(" ")
            date = f"{date[4][:3]} {date[5]} {date[6]}"
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
            return None
    
    def nasdaq(self, url: str) -> dict:
        body = super()._get_html(url)
        try:
            text_body = super()._strip_emojies(body.find("div", class_="body__content").text).strip()

            return {
                "url": url,
                "provider": "nasdaq",
                "title": body.find("h1", class_="article-header__headline").text,
                "text_body": text_body,
                "hits": super()._process_text_body(text_body),
                "datetime": body.find("time")["datetime"][:-5]
            }
            
        except Exception as e:
            print(e)
            print(url)
            return None