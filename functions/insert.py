from functions.format_timing import format_timing
from stockTracker import Stock

def insert_tracking(db: object, symbol: str, last_price: float, min_price: float, max_price: float, volume: int, timing: str) -> None:
    """
        Inserts tracking into db.
    """
    result = db.get_todays_tracking(symbol)

    # if stock already registered in analytics, return
    if result: return
    
    timing = format_timing(timing)
    db.insert_tracking(symbol, last_price, min_price, max_price, volume, timing)

def insert_stock(db: object, seen_stocks: dict, symbol: str, company_name: str, exchange: str) -> None:
    """
        Inserts stock into db.
    """
    if symbol in seen_stocks: 
        seen_stocks[symbol].increment(1)
        db.update_stock(seen_stocks[symbol])
    else:
        stock = Stock(company_name, symbol, exchange)
        db.insert_stock(stock)
        seen_stocks[symbol] = stock
