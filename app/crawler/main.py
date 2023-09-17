import asyncio

from app.http import http, build_url, Proxy
from app.crawler.crawler import crawl_articles
from settings import API_URL



def crawl():
    proxy = Proxy

    crawl_articles(
        "https://cnn.com",
        "https://cnn.com",
        "CNN",
        [],
        [],
        proxy
    )