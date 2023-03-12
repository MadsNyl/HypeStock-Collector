from db.setup import pool, db
from db.model import Query

class INSERT():

    @staticmethod
    def stock(symbol: str, title: str, exchange: str):
        """
            Inserts a stock.
        """
        try:
            pool.execute(
                Query.insert_stock(),
                (
                    symbol,
                    title,
                    exchange
                )
            )
            
            db.commit()
        except Exception as e:
            print(f"Stock insertion error: {e}")
    
    @staticmethod
    def article(provider: str, external: bool, title: str, url: str, body: str, created_date: str):
        """
            Inserts article.
        """
        try:
            pool.execute(
                Query.insert_article(),
                (
                    provider,
                    external,
                    title,
                    url,
                    body,
                    created_date
                )
            )

            db.commit()
            return pool._last_insert_id
        except Exception as e:
            print(f"Inserting article error: {e}")
    
    @staticmethod
    def article_stock(symbol: str, article_id: int):
        """
            Inserts relation between stock and article.
        """
        try:
            pool.execute(
                Query.insert_article_stock(),
                (
                    symbol,
                    article_id
                )
            )

            db.commit()
        except Exception as e:
            print(f"Inserting article_stock error: {e}")