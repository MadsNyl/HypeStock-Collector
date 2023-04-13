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
    
    @staticmethod
    def legacy_stocks():
        """
            Returns all stocks that have not collected legacy data.
        """
        try:
            pool.execute(
                Query.get_legacy_stocks()
            )

            return pool.fetchall()
        except Exception as e:
            print(f"Fetching all legacy stocks error: {e}")
    
    @staticmethod
    def tickers():
        """
            Returns all tickers.
        """
        try:
            pool.execute(
                Query.get_stocks()
            )

            return dict.fromkeys(list(map(lambda x: x[0], pool.fetchall())))
        except Exception as e:
            print(f"Fetching all tickers error: {e}")
    
    @staticmethod
    def comment_urls():
        """
            Returns all comment urls.
        """
        try:
            pool.execute(
                Query.get_comment_urls()
            )

            return dict.fromkeys(list(map(lambda x: x[0], pool.fetchall())))
        except Exception as e:
            print(f"Fetching comment urls error: {e}")
    
    @staticmethod
    def article_urls():
        """
            Returns all article urls.
        """
        try:
            pool.execute(
                Query.get_article_urls()
            )

            return dict.fromkeys(list(map(lambda x: x[0], pool.fetchall())))
        except Exception as e:
            print(f"Fetching all article urls error: {e}")
    
    @staticmethod
    def subreddits():
        """
            Returns all subdreddits.
        """
        try:
            pool.execute(
                Query.get_subreddits()
            )

            return pool.fetchall()
        except Exception as e:
            print(f"Fetching all subreddists error: {e}")
    
    @staticmethod
    def last_tracking_date():
        """
            Returns last tracking date added.
        """
        try:
            pool.execute(
                Query.get_last_tracking_date()
            )

            return pool.fetchone()
        except Exception as e:
            print(f"Fetching tracking error: {e}")