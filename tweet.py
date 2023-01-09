class Tweet():
    
    @staticmethod
    def create(tweet: object, symbol: str, score: float) -> object:
        obj = {}
        obj["symbol"] = symbol
        obj["url"] = tweet.url
        obj["author"] = tweet.user.username
        obj["like_count"] = tweet.likeCount
        obj["retweet_count"] = tweet.retweetCount
        obj["reply_count"] = tweet.replyCount
        obj["quote_count"] = tweet.quoteCount
        obj["score"] = score
        obj["date"] = tweet.date

        return obj
    
    @staticmethod
    def check_like_count(tweet: object) -> bool:
        if tweet.likeCount < 10: return False
        return True