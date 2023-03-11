from crawler import ArticleCrawler

URLS = [
    "https://edition.cnn.com/business",
    "https://finance.yahoo.com/topic/stock-market-news/",
    "https://www.cnbc.com/finance/"
]

if __name__ == "__main__":
    a = ArticleCrawler(URLS)
    a.run()