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
    def get_stock_info():
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
    def get_legacy_stocks():
        """
            Returns all stock that have not collected legacy data.
        """
        try:
            pool.execute(
                Query.get_legacy_stocks()
            )

            return pool.fetchall()
        except Exception as e:
            print(f"Fetching all legacy stocks error: {e}")

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
    def get_subreddits():
        """
            Gets all subreddits.
        """
        try:
            pool.execute(
                Query.get_subreddits()
            )

            return pool.fetchall()
        except Exception as e:
            print(f"Fetching all subreddists error: {e}")
        
    @staticmethod
    def get_article_url(url: str):
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

    @staticmethod
    def update_legacy(symbol: str):
        """
            Updates legacy for a symbol to true.
        """
        try:
            pool.execute(
                Query.update_legacy(),
                (symbol, )
            )

            db.commit()
        except Exception as e:
            print(f"Updating legacy error: {e}")
        
    @staticmethod
    def insert_article(provider: str, external: bool, title: str, url: str, body: str, created_date: str):
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
    def insert_article_stock(symbol: str, article_id: int):
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