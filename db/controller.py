from db.setup import pool, db
from db.model import Query

class API():

    @staticmethod
    def get_stock(symbol: str):
        """
            Returns stock based on symbol.
        """
        try:
            pool.execute(
                Query.get_stock(),
                (symbol, )
            )

            return pool.fetchone()
        except Exception as e:
            print(f"Fetching stock error:\n{e}")

    @staticmethod
    def get_comments(urls: list[str]):
        """
            Gets all comments that match with given urls.
        """
        try:
            pool.execute(
                Query.get_comments(len(urls)),
                tuple(urls)
            )

            return pool.fetchall()
        except Exception as e:
            print(f"Fetching comments error:\n{e}")

    @staticmethod
    def insert_comment(symbol: str, neg_score: float, neu_score: float, pos_score: float, subreddit: str, post_url: str, permalink: str, body: str, author: str, created_date: str):
        """
            Inserts a comment from Reddit.
        """
        try:
            pool.execute(
                Query.insert_comment(),
                (
                    symbol,
                    post_url,
                    permalink,
                    subreddit,
                    created_date,
                    body,
                    author,
                    neg_score,
                    neu_score,
                    pos_score
                )
            )

            db.commit()
        except Exception as e:
            print(f"Comment insertion error:\n{e}")

    @staticmethod
    def insert_stock(symbol: str, title: str, exchange: str):
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
            print(f"Stock insertion error:\n{e}")
