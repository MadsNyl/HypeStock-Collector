from db.setup import pool, db
from db.model import Query

class API():

    @staticmethod
    def get_stocks():
        """
            Returns all stocks.
        """
        try:
            pool.execute(
                Query.get_stocks()
            )

            return pool.fetchall()
        except Exception as e:
            print(f"Fetching all stocks error: {e}")


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
            print(f"Fetching stock error: {e}")
    
    @staticmethod
    def get_tracking(symbol: str):
        """
            Returns a tracked timing based on symbol.
        """
        try:
            pool.execute(
                Query.get_tracking(),
                (symbol, )
            )

            return pool.fetchone()
        except Exception as e:
            print(f"Fetching tracking error: {e}")
        
    
    @staticmethod
    def get_tweet(url: str):
        """
            Gets symbol of tweet based on url.
        """
        try:
            pool.execute(
                Query.get_tweet(),
                (url, )
            )

            return pool.fetchone()
        except Exception as e:
            print(f"Fetching tweet error: {e}")

    @staticmethod
    def get_comments(urls: list[str]):
        """
            Gets all comments that match with given urls.
        """
        try:
            if len(urls) == 0: return
            
            pool.execute(
                Query.get_comments(len(urls)),
                tuple(urls)
            )

            return pool.fetchall()
        except Exception as e:
            print(f"Fetching comments error: {e}")

    @staticmethod
    def insert_comment(symbol: str, neg_score: float, neu_score: float, pos_score: float, subreddit: str, post_url: str, permalink: str, body: str, author: str, created_date: str, likes: int):
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
                    pos_score,
                    likes
                )
            )

            db.commit()
        except Exception as e:
            print(f"Comment insertion error: {e}")

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
            print(f"Stock insertion error: {e}")

    @staticmethod
    def insert_tweet(tweet: object):
        """
            Inserts a tweet.
        """
        try:
            pool.execute(
                Query.insert_tweet(),
                (
                    tweet["symbol"],
                    tweet["url"],
                    tweet["body"],
                    tweet["author"],
                    tweet["like_count"],
                    tweet["retweet_count"],
                    tweet["reply_count"],
                    tweet["quote_count"],
                    tweet["negative_score"],
                    tweet["neutral_score"],
                    tweet["positive_score"],
                    tweet["date"]
                )
            )

            db.commit()
        except Exception as e:
            print(f"Tweet insertion error: {e}")
    
    @staticmethod
    def insert_trackings(data: list):
        """
            Inserts a list of trackings.
        """
        try:
            pool.executemany(
                Query.insert_trackings(),
                data
            )

            db.commit()
        except Exception as e:
            print(f"Trackings insertion error: {e}")