import snscrape.modules.twitter as sntwitter
from db.db import DB
from models.stock import Stock
from util.progress_bar import print_progress_bar, print_progress_bar_objects
from util.valid_symbol import is_string_valid
from util.get_stock_data import get_stock_data
from util.sentiment_analyzis import analyze
from util.insert import insert_stock, insert_tracking
from models.tweet import Tweet

class TwitterUser():

    tweets: list
    limit: int
    username: str
    db: DB = DB()
    data: list[dict] = []
    seen_stocks = dict[str: Stock]

    def __init__(self, usernames: list[str], limit: int):
        self.usernames = usernames
        self.seen_stocks = self.db.update_record()
        self.limit = limit

    def run(self) -> None:
        for username in self.usernames:
            tweets = sntwitter.TwitterUserScraper(username).get_items()
            self.collect_tweets(tweets)

    def collect_tweets(self, tweets: list) -> None:        
        for i, tweet in enumerate(tweets):
            if i >= self.limit: break
            self.data.append(tweet)

    def process_data(self) -> None:
        l = len(self.data)
        
        print_progress_bar_objects(l)
        for i, tweet in enumerate(self.data):
            self.process_content(tweet)
            print_progress_bar(i + 1, l)
    
    def process_content(self, tweet: object) -> None:
        for string in tweet.content.strip().split(" "):
            string = string.replace("$", "")
            if not is_string_valid(string): continue

            # check if tweet has been seen before
            if self.db.tweet_seen(tweet.url): continue

            # check if symbol exsist and get info
            result = self.db.check_symbol(string)
            if not result:
                company_name, exchange = get_stock_data(string) 
                if company_name is None: continue
            
            else: 
                company_name = result[0][0]
                exchange = result[0][1]

            # get sentiment score of content text
            scores = analyze(tweet.content)

            # insert stock in db
            insert_stock(self.db, self.seen_stocks, string, company_name, exchange)

            # create tweet object
            tweet_obj = Tweet.create(tweet, string, scores)

            # insert tweet
            self.db.insert_tweet(tweet_obj)