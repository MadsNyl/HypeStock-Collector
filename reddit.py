from settings.credentials import reddit
from stockTracker import Stock
from db import DB
from nltk.sentiment import SentimentIntensityAnalyzer
from functions.progress_bar import print_progress_bar, print_progress_bar_subs, print_progress_bar_objects
from functions.valid_symbol import is_string_valid
from functions.get_stock_data import get_stock_data
from functions.sentiment_analyzis import analyze
from functions.insert import insert_stock, insert_tracking
import nltk

class Reddit():

    subreddit: reddit.subreddit
    seen_stocks: dict[str: Stock]
    limit: int
    db: DB = DB()
    data: list[dict] = []
    sia: SentimentIntensityAnalyzer

    def __init__(self, subreddit, limit) -> None:
        self.subreddit = reddit.subreddit(subreddit)
        self.limit = limit
        self.seen_stocks = self.db.update_record()
        nltk.download("vader_lexicon")
        self.sia = SentimentIntensityAnalyzer()
    
    def run(self) -> None:
        
        # print start of progress bar
        print_progress_bar_subs(self.limit)

        # iterate through all subs collected
        for i, sub in enumerate(self.subreddit.hot(limit=self.limit)):
            sub.comments.replace_more(limit=0)

            # get reddit post url
            post_url = sub.permalink

            # process comments
            self.process_comments(sub.comments.list(), post_url)

            # update progress bar
            print_progress_bar(i + 1, self.limit)            

    def process_comments(self, comments: list, post_url: str) -> None:
        for comment in comments:
            # store data in object
            url = comment.permalink
            body = comment.body
            author = comment.author

            # check if author exists
            if author: author = author.name

            # split comment body in strings
            strings = comment.body.strip().split(" ")
            
            # process comment body
            self.process_body(strings, url, body, author, post_url)
    
    def process_body(self, comment_body: list[str], url: str, body: str, author: str, post_url: str) -> None:
        obj = {}
        for string in comment_body:
            # check if string is a stock symbol
            if is_string_valid(string):
                # store data
                self.store_data(obj, post_url, string, author, url, body)
                break

    def store_data(self, obj: dict[str: str], post_url: str, string: str, author: str, url: str, body: str) -> None:
        obj["post_url"] = post_url
        obj["symbol"] = string
        obj["author"] = author
        obj["comment_url"] = url
        obj["comment_body"] = body
        self.data.append(obj)

    def proccess_data(self):
        l = len(self.data)
        print_progress_bar_objects(l)
        for i, obj in enumerate(self.data):
            company_name, last_price, min_price, max_price, volume, timing, _, _ = get_stock_data(obj["symbol"])  
            if company_name is None: continue

            # if comment already is in db, continue
            if self.db.reddit_comment_seen(obj["comment_url"]): continue

            # get sentiment score of comment text
            sentiment_score = analyze(obj["comment_body"])

            # insert stock to db
            insert_stock(self.db, self.seen_stocks, obj["symbol"], company_name)
            
            # insert sentiment to db
            self.db.insert_sentiment(obj["symbol"], sentiment_score, True, obj["post_url"], obj["comment_url"], obj["comment_body"], obj["author"])

            # insert tracking to db
            insert_tracking(self.db, obj["symbol"], last_price, min_price, max_price, volume, timing)

            # update progress bar
            print_progress_bar(i + 1, l)
