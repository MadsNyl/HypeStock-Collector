import snscrape.modules.twitter as sntwitter
from db import DB
from stockTracker import Stock
from nltk.sentiment import SentimentIntensityAnalyzer
from functions.progress_bar import print_progress_bar, print_progress_bar_objects
from functions.valid_symbol import is_string_valid
from functions.get_stock_data import get_stock_data
from functions.sentiment_analyzis import analyze
from functions.insert import insert_stock, insert_tracking
from tweet import Tweet
import nltk


class Twitter():

    tweets: list
    hashtag: str
    limit: int
    db: DB = DB()
    data: list[dict] = []
    seen_stocks = dict[str: Stock]
    sia: SentimentIntensityAnalyzer

    def __init__(self, hashtag, limit) -> None:
        self.tweets = sntwitter.TwitterHashtagScraper(hashtag).get_items()
        self.limit = limit
        self.likeLimit = 10
        self.seen_stocks = self.db.update_record()
        nltk.download("vader_lexicon")
        self.sia = SentimentIntensityAnalyzer()

    
    def run(self) -> None:
        self.collect_tweets()

    def collect_tweets(self) -> None:        
        for i, tweet in enumerate(self.tweets):
            if i > self.limit: break
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
        for string in tweet.content.strip().split(" "):
            string = string.replace("$", "")
            if not is_string_valid(string): continue

            # check if tweet has been seen before
            if self.db.tweet_seen(tweet.url): continue

            # check if symbol exsist and get info
            company_name, last_price, min_price, max_price, volume, timing, _, _ = get_stock_data(string) 

            if company_name is None: continue

            # get sentiment score of content text
            sentiment_score = analyze(tweet.content)

            # insert stock in db
            insert_stock(self.db, self.seen_stocks, string, company_name)

            # create tweet object
            tweet_obj = Tweet.create(tweet, string, sentiment_score)

            # insert tweet
            self.db.insert_tweet(tweet_obj)

            # insert tracking in db
            insert_tracking(self.db, string, last_price, min_price, max_price, volume, timing)