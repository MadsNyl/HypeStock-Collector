
class Query():

    @staticmethod
    def get_stock() -> str:
        return """
            SELECT symbol, exchange
            FROM stock
            WHERE symbol = %s
        """
    
    @staticmethod
    def get_tweet() -> str:
        return """
            SELECT symbol
            FROM tweet
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
    def insert_comment() -> str:
        return """
            INSERT INTO comment
            (symbol, post_url, permalink, subreddit, created_date, body, author, negative_score, neutral_score, positive_score)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
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