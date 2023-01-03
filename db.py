import mysql.connector
from settings.db_settings import DATABASE, DB_PASSWORD, DB_HOST, DB_USERNAME
from stockTracker import Stock


class DB():
    def __init__(self):
        self.db = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USERNAME,
            password=DB_PASSWORD,
            database=DATABASE
        )
        self.pool = self.db.cursor(buffered=True)

    def reconnect(self) -> None:
        try:
            print("Reconnecting db.")
            self.db = mysql.connector.connect(
                host=DB_HOST,
                user=DB_USERNAME,
                password=DB_PASSWORD,
                database=DATABASE
            )

            self.pool = self.db.cursor(buffered=True)
        except Exception as e:
            print(e)

    def check_connection(self) -> bool:
        if self.db.is_connected(): return
        
        self.reconnect()
        return False
    
    def get_todays_tracking(self, symbol: str) -> tuple:
        try:
            self.check_connection()
            self.pool.execute(
                "SELECT symbol FROM analytic WHERE symbol = %s ORDER BY timing DESC",
                (symbol, )
            )
            result = self.pool.fetchone()
            return result
        except Exception as e:
            print(e)
            print(f"Analytics search failed. Could not find {symbol}")
    
    def insert_tracking(self, symbol: str, last_price: str, min_price: str, max_price: str, volume: str, timing: str) -> None:
        try:
            self.check_connection()

            self.pool.execute(
                "INSERT into analytic (symbol, last_price, min_price, max_price, volume, timing) VALUES (%s, %s, %s, %s, %s, %s)",
                (symbol, float(last_price[1:]), float(min_price[1:]), float(max_price[1:]), int(volume.replace(",", "")), timing)
            )
            self.db.commit()
        except Exception as e:
            print(e)
            print("Insertion of analytic failed.")
    
    def insert_stock(self, stock: Stock) -> None:
        try:
            self.check_connection()

            if (self.stock_exist(stock.getSymbol()) == False):
                self.pool.execute(
                        "INSERT INTO stock (symbol, name, reference_count) VALUES (%s, %s, %s)",
                        (stock.getSymbol(), stock.getTitle(), stock.getCount())
                    )
                self.db.commit()
        except Exception as e:
            print(e) 
            print("Insertion failed.")

    def update_stock(self, stock: Stock) -> None:
        try:
            self.check_connection()

            self.pool.execute(
                    "UPDATE stock SET reference_count = %s WHERE symbol = %s",
                    (stock.getCount(), stock.getSymbol())
                )
            self.db.commit()
        except:
            print("Update failed.")

    def stock_exist(self, symbol: str) -> bool:
        try:
            self.check_connection()

            self.pool.execute(
                "SELECT * FROM stock WHERE symbol = %s",
                (symbol, )
            )

            result = self.pool.fetchone()
            if result: return True
            return False
        except Exception as e:
            print(e)
            print("search failed")
    
    def update_record(self) -> dict:
        seen_stocks = {}

        try:
            self.check_connection()

            self.pool.execute(
                "SELECT * FROM stock"
            )
            results = self.pool.fetchall()
            
            if len(results) <= 0: return seen_stocks

            for result in results:
                stock = Stock(result[1], result[0])
                stock.increment(result[2] - 1)
                seen_stocks[result[0]] = stock
        except:
            print("Update of records failed.")

        return seen_stocks
    
    def insert_sentiment(self, symbol: str, score: float, is_reddit: str, post_url: str, permalink: str, comment_body: str, author: str) -> None:
        try:
            self.check_connection()

            self.pool.execute(
                "INSERT INTO sentiment (symbol, score, is_reddit, post_url, permalink, comment_body, author) VALUES(%s, %s, %s, %s, %s, %s, %s)",
                (symbol, score, is_reddit, post_url, permalink, comment_body, author)
            )
            self.db.commit()
        except Exception as e:
            pass
            # print(e)
            # print("Insertion of sentiment failed.")
    
    def get_all_stocks(self) -> tuple:
        try:
            self.check_connection()

            self.pool.execute(
                "SELECT symbol FROM stock"
            )
            results = self.pool.fetchall()
            return results
        except Exception as e:
            print(e)
    
    def get_all_analytic_dates(self) -> tuple:
        try:
            self.check_connection()

            self.pool.execute(
                "SELECT symbol, timing FROM analytic ORDER BY timing DESC"
            )
            results = self.pool.fetchall()
            return results
        except Exception as e:
            print(e)
    
    def update_analytics(self, symbols: list[str]) -> None:
        try:
            self.check_connection()

            self.pool.executemany(
                "INSERT INTO analytic (symbol, last_price, min_price, max_price, volume, timing, price_change, price_change_pct) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
                symbols
            )
            self.db.commit()
        except Exception as e:
            print(e)
            pass
    
    def get_analytic(self, symbol: str) -> tuple:
        try:
            self.check_connection()

            self.pool.execute(
                "SELECT timing FROM analytic WHERE symbol = %s ORDER BY timing DESC LIMIT 1",
                (symbol, )
            )

            result = self.pool.fetchone()
            return result
        except Exception as e:
            print(e)