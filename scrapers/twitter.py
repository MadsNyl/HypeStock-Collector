import snscrape.modules.twitter as sntwitter
import tweepy
from db.db import DB
from models.stock import Stock
from scrapers.settings import twitter
from functions.progress_bar import print_progress_bar, print_progress_bar_objects
from functions.valid_symbol import is_string_valid
from functions.get_stock_data import get_stock_data
from functions.sentiment_analyzis import analyze
from functions.insert import insert_stock, insert_tracking
from models.tweet import Tweet

class Twitter():

    tweets: list
    db: DB = DB()
    data: list[object] = []
    seen_stocks = dict[str: Stock]

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
        self.seen_stocks = self.db.update_record()
    
    def run(self) -> None:
        self.collect_tweets()

    def collect_tweets(self) -> None:  
        for i, tweet in enumerate(self.tweets):
            self.data.append(tweet)
    
    def process_data(self) -> None:
        l = len(self.data)
        
        print_progress_bar_objects(l)
        for i, tweet in enumerate(self.data):
            # check for like limit
            if not Tweet.check_like_count(tweet): continue
            self.process_content(tweet)
            print_progress_bar(i + 1, l)

    def process_content(self, tweet: object) -> None:
        for string in tweet.text.strip().split(" "):
            string = string.replace("$", "")
            if not is_string_valid(string): continue

            # build url 
            url = Tweet.build_url(tweet)

            # check if tweet has been seen before
            if self.db.tweet_seen(url): continue

            # check if symbol exsist and get info
            result = self.db.check_symbol(string)
            if not result:
                company_name, exchange = get_stock_data(string) 
                if company_name is None: continue
            
            else: 
                company_name = result[0][0]
                exchange = result[0][1]

            # get sentiment score of content text
            scores = analyze(tweet.text)

            # insert stock in db
            insert_stock(self.db, self.seen_stocks, string, company_name, exchange)

            # create tweet object
            tweet_obj = Tweet.create(tweet, string, scores)

            # insert tweet
            self.db.insert_tweet(tweet_obj)
