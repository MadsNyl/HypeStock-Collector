from scrapers.settings import reddit
from models.stock import Stock
from db.db import DB
from functions.progress_bar import print_progress_bar, print_progress_bar_subs, print_progress_bar_objects
from functions.valid_symbol import is_string_valid
from functions.get_stock_data import get_stock_data
from functions.sentiment_analyzis import analyze
from functions.insert import insert_stock, insert_tracking
from functions.validate_post import validate_reddit_comment
from models.comment import Comment

class Reddit():

    subreddit: reddit.subreddit
    seen_stocks: dict[str: Stock]
    limit: int
    db: DB = DB()
    data: list[dict] = []

    def __init__(self, subreddit, limit) -> None:
        self.subreddit = reddit.subreddit(subreddit)
        self.sub = subreddit
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
        # check if any comments already are in db
        sorted_data = validate_reddit_comment(self.db, self.data)

        if len(sorted_data) == 0: 
            print("All comments allready registered.")
            return

        l = len(sorted_data)
        print_progress_bar_objects(l)
        for i, obj in enumerate(sorted_data):
            # if symbol already is in db, skip fetching stock data
            result = self.db.check_symbol(obj["symbol"])
            if not result:
                company_name, exchange = get_stock_data(obj["symbol"])  
                if company_name is None: continue
            
            else: 
                company_name = result[0][0]
                exchange = result[0][1]

            try:
                # get sentiment score of comment text
                scores = analyze(obj["comment_body"])
            except Exception as e:
                print(e)
                continue

            # insert stock to db
            insert_stock(self.db, self.seen_stocks, obj["symbol"], company_name, exchange)
            
            # # insert sentiment to db
            self.db.insert_comment(obj["symbol"], scores["neg"], scores["neu"], scores["pos"], self.sub, obj["post_url"], obj["comment_url"], obj["comment_body"], obj["author"], obj["created_date"])

            # update progress bar
            print_progress_bar(i + 1, l)
