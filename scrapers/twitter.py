import snscrape.modules.twitter as sntwitter
import tweepy
from db.controller import API
from models.stock import Stock
from scrapers.settings import twitter
from util.progress_bar import progressbar
from util.valid_symbol import is_string_valid
from util.get_stock_data import get_stock_data
from util.sentiment_analyzis import analyze
from util.remove_emojies import remove_emojies
from models.tweet import Tweet

class Twitter():

    tweets: list
    data: list[object] = []

    def __init__(self, query: str, limit: int) -> None:
        self.tweets = tweepy.Paginator(
            twitter.search_recent_tweets,
            query=query,
            max_results=100,
            tweet_fields=[
                "author_id",
                "created_at",
                "text",
                "public_metrics"
            ]
        ).flatten(limit=limit)
        self.limit = limit
    
    def run(self) -> None:
        self.collect_tweets()

    def collect_tweets(self) -> None:  
        for i, tweet in enumerate(self.tweets):
            self.data.append(tweet)
    
    def process_data(self) -> None:
        l = len(self.data)
        
        progressbar(0, l, f"Proccessing {l} tweets: ")
        for i, tweet in enumerate(self.data):
            if not Tweet.check_like_count(tweet): continue
            self.process_content(tweet)
            progressbar(i + 1, l, None)
    
    def stripped_tweet(self, tweet: object) -> None: return tweet.strip().split(" ")

    def process_content(self, tweet: object) -> None:
        body = remove_emojies(tweet.text)
        for string in self.stripped_tweet(body):
            string = string.replace("$", "")
            if not is_string_valid(string): continue

            url = Tweet.build_url(tweet)

            if API.get_tweet(url): continue

            result = API.get_stock(string)
            if result is None:
                company_name, exchange = get_stock_data(string) 
                if company_name is None: continue
                else: API.insert_stock(string, company_name, exchange)
            
            else: 
                company_name = result[0][0]
                exchange = result[0][1]

            try: scores = analyze(tweet.text)
            except Exception as e:
                print(f"Sentiment analyzis error: {e}")
                continue

            API.insert_tweet(
                Tweet.create(tweet, string, scores, body)
            )
