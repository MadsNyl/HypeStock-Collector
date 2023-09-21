import asyncio

from app.http import http, build_url, Proxy
from app.crawler.crawler import crawl_articles
from app.classes import Newspaper



def crawl():

    article_urls = crawl_articles(
        Newspaper(
            id=1,
            provider="cnn",
            name="CNN",
            start_url="https://edition.cnn.com/business",
            base_url="https://edition.cnn.com"
        )
    )

    