from scrapers import Yahoo

if __name__ == "__main__":
    a = Yahoo(
        base_url="https://finance.yahoo.com/topic/stock-market-news/"
    )
    a.run()