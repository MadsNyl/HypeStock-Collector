from settings.credentials import twitter

class Tweet():
    
    @staticmethod
    def create(tweet: object, symbol: str, scores: float) -> object:
        obj = {}
        obj["symbol"] = symbol
        obj["url"] = Tweet.build_url(tweet)
        obj["author"] = Tweet.get_author(tweet)
        obj["like_count"] = tweet.public_metrics["like_count"]
        obj["retweet_count"] = tweet.public_metrics["retweet_count"]
        obj["reply_count"] = tweet.public_metrics["reply_count"]
        obj["quote_count"] = tweet.public_metrics["quote_count"]
        obj["negative_score"] = scores["neg"]
        obj["neutral_score"] = scores["neu"]
        obj["positive_score"] = scores["pos"]
        obj["date"] = tweet.created_at

        return obj
    
    @staticmethod
    def check_like_count(tweet: object) -> bool:
        if tweet.public_metrics["like_count"] <= 5: return False
        return True

    @staticmethod
    def get_author(tweet: object) -> str:
        id = tweet.author_id
        author = twitter.get_user(id=id)
        return author.data.username

    @staticmethod
    def build_url(tweet: object) -> str:
        id = tweet.id
        return f"https://twitter.com/twitter/statuses/{id}"
