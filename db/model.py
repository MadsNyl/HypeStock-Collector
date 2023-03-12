
class Query():

    @staticmethod
    def get_stocks() -> str:
        return """
            SELECT symbol
            FROM stock
        """

    @staticmethod
    def get_subreddits() -> str:
        return """
            SELECT DISTINCT subreddit
            FROM comment
        """
    
    @staticmethod
    def get_stock_info() -> str:
        return """
            SELECT symbol, name
            FROM stock
        """
    
    @staticmethod
    def get_legacy_stocks() -> str:
        return """
            SELECT symbol
            FROM stock 
            WHERE legacy = false
        """

    @staticmethod
    def get_stock() -> str:
        return """
            SELECT symbol, exchange
            FROM stock
            WHERE symbol = %s
        """
    
    @staticmethod
    def get_tracking() -> str:
        return """
            SELECT timing
            FROM tracking
            WHERE symbol = %s
            ORDER BY timing DESC
        """
    
    @staticmethod
    def get_tweet() -> str:
        return """
            SELECT symbol
            FROM tweet
            WHERE url = %s
        """
    
    @staticmethod
    def get_article_url() -> str:
        return """
            SELECT url
            FROM article
            WHERE url = %s
        """
    
    @staticmethod
    def get_comments(length: int) -> str:
        return f"""
            SELECT permalink
            FROM comment
            WHERE permalink IN ({','.join(['%s'] * length)})
        """
    
    @staticmethod
    def get_comment_urls() -> str:
        return """
            SELECT permalink
            FROM comment
        """

    @staticmethod
    def insert_comment() -> str:
        return """
            INSERT INTO comment
            (symbol, post_url, permalink, subreddit, created_date, body, author, negative_score, neutral_score, positive_score, likes)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
    
    @staticmethod
    def insert_stock() -> str:
        return """
            INSERT INTO stock
            (symbol, name, exchange)
            VALUES(%s, %s, %s)
        """
    
    @staticmethod
    def insert_tweet() -> str:
        return """
            INSERT INTO tweet
            (symbol, url, body, author, likes, retweets, replies, quotes, negative_score, neutral_score, positive_score, created_date)
            VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
    
    @staticmethod
    def insert_trackings() -> str:
        return """
            INSERT INTO tracking
            (symbol, last_price, min_price, max_price, volume, timing, price_change, price_change_pct)
            VALUES(%s, %s, %s, %s, %s, %s, %s, %s)
        """
    
    @staticmethod
    def update_legacy() -> str:
        return """
            UPDATE stock
            SET legacy = true
            WHERE symbol = %s
        """
    
    @staticmethod
    def insert_article() -> str:
        return """
            INSERT INTO article
            (provider, external, title, url, body, created_date)
            VALUES(%s, %s, %s, %s, %s, %s)
        """
    
    @staticmethod
    def insert_article_stock() -> str:
        return """
            INSERT INTO article_stock
            (symbol, article_id)
            VALUES(%s, %s)
        """

    @staticmethod
    def insert_tracking() -> str:
        return """
            INSERT INTO tracking
            (symbol, last_price, volume, marketcap, price_change_pct)
            VALUES (%s, %s, %s, %s, %s)
        """