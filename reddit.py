from settings.credentials import reddit
from stockTracker import Stock
from db import DB
from functions.progress_bar import print_progress_bar, print_progress_bar_subs, print_progress_bar_objects
from functions.valid_symbol import is_string_valid
from functions.get_stock_data import get_stock_data
from functions.sentiment_analyzis import analyze
from functions.insert import insert_stock, insert_tracking
from comment import Comment

class Reddit():

    subreddit: reddit.subreddit
    seen_stocks: dict[str: Stock]
    limit: int
    db: DB = DB()
    data: list[dict] = []

    def __init__(self, subreddit, limit) -> None:
        self.subreddit = reddit.subreddit(subreddit)
        self.limit = limit
        self.seen_stocks = self.db.update_record()
    
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
            # process comment body
            self.process_body(comment, post_url)
    
    def process_body(self, comment: object, post_url: str) -> None:
        for string in comment.body.strip().split(" "):
            # check if string is a stock symbol
            if is_string_valid(string):
                # store data
                obj = Comment.create(comment, string, post_url)
                self.data.append(obj)
                break

    def proccess_data(self):
        l = len(self.data)
        print_progress_bar_objects(l)
        for i, obj in enumerate(self.data):
            # if comment already is in db, continue
            if self.db.reddit_comment_seen(obj["comment_url"]): continue

            # if symbol already is in db, skip fetching stock data
            company_name = self.db.check_symbol(obj["symbol"])
            if not company_name:
                company_name = get_stock_data(obj["symbol"])  
                if company_name is None: continue
            
            company_name = company_name[1]

            # get sentiment score of comment text
            scores = analyze(obj["comment_body"])

            # insert stock to db
            insert_stock(self.db, self.seen_stocks, obj["symbol"], company_name)
            
            # # insert sentiment to db
            self.db.insert_sentiment(obj["symbol"], scores["neg"], scores["neu"], scores["pos"],  True, obj["post_url"], obj["comment_url"], obj["comment_body"], obj["author"], obj["created_date"])

            # update progress bar
            print_progress_bar(i + 1, l)
