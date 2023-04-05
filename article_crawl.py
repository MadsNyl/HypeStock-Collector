from crawler import ArticleCrawler

URLS = [
    "https://edition.cnn.com/business",
    "https://www.nasdaq.com/news-and-insights/markets",
    "https://finance.yahoo.com/topic/stock-market-news/",
    "https://www.cnbc.com/finance/",
    "https://www.ft.com/markets",
]

if __name__ == "__main__":
    a = ArticleCrawler(URLS)
    a.run()