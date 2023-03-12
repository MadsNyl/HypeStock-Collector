import requests
from db import INSERT
from util import progressbar

def get_data(url: str) -> list:
    res = requests.get(url)
    return res.json()
    
def main(url: str, exchange: str) -> None:
    json = get_data(url)
    progressbar(0, len(json), f"Inserting trackings from {exchange}: ")
    for i, object in enumerate(json):
        INSERT.tracking(
            symbol=object["symbol"],
            last_price=float(object["lastsale"][1:]) if len(object["lastsale"][1:]) else None,
            volume=int(object["volume"]) if len(object["volume"]) else None,
            marketcap=int(float(object["marketCap"])) if len(object["marketCap"]) else None,
            price_change_pct=float(object["pctchange"][:-1]) if len(object["pctchange"][:-1]) else None
        )
        progressbar(i + 1, len(json), None)


if __name__ == "__main__":
    stock_data = [
        { "url": "https://raw.githubusercontent.com/rreichel3/US-Stock-Symbols/main/amex/amex_full_tickers.json", "exchange": "amex" },
        { "url": "https://raw.githubusercontent.com/rreichel3/US-Stock-Symbols/main/nasdaq/nasdaq_full_tickers.json", "exchange": "nasdaq" },
        { "url": "https://raw.githubusercontent.com/rreichel3/US-Stock-Symbols/main/nyse/nyse_full_tickers.json", "exchange": "nyse"}
    ]

    for data in stock_data:
        main(data["url"], data["exchange"])