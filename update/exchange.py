from db.db import DB
from util.get_stock_data import get_stock_data

db = DB()
all_stocks = db.update_record()

print(len(all_stocks))
for i, stock in enumerate(all_stocks):  
    _, exchange = get_stock_data(stock)
    print(f"Inserting {stock} with {exchange} as number {i}")
    db.update_exchange(stock, exchange)
