from db.setup import pool, db
from db.model import Query

class GET():

    @staticmethod
    def article_url(url: str):
        """
            Checks for url match.
        """
        try:
            pool.execute(
                Query.get_article_url(),
                (url, )
            )

            return pool.fetchone()
        except Exception as e:
            print(f"Fetching article url match error: {e}")
    
    @staticmethod
    def stock_info():
        """
            Returns all stocks with ticker and name.
        """
        try:
            pool.execute(
                Query.get_stock_info()
            )

            return pool.fetchall()
        except Exception as e:
            print(f"Fetching all stocks with info error: {e}")