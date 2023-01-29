from scrapers.settings import reddit
from db.controller import API 
from functions.progress_bar import progressbar
from functions.valid_symbol import is_string_valid
from functions.get_stock_data import get_stock_data
from functions.sentiment_analyzis import analyze
from functions.validate_comment import parse_comments
from functions.remove_emojies import remove_emojies
from models.comment import Comment

class Reddit():

    subreddit: reddit.subreddit
    limit: int
    data: list[dict] = []

    def __init__(self, subreddit, limit) -> None:
        self.subreddit = reddit.subreddit(subreddit)
        self.sub = subreddit
        self.limit = limit
    
    def run(self) -> None:

        progressbar(0, self.limit, f"Collecting {self.limit} subreddits: ")

        for i, sub in enumerate(self.get_subreddits()):
            sub.comments.replace_more(limit=0)

            post_url = sub.permalink

            self.process_comments(sub.comments.list(), post_url)

            progressbar(i + 1, self.limit, None)       

    def get_subreddits(self) -> list: return self.subreddit.hot(limit=self.limit)     

    def process_comments(self, comments: list, post_url: str) -> None:
        for comment in comments: self.process_body(comment, post_url)
    
    def process_body(self, comment: object, post_url: str) -> None:
        body = remove_emojies(comment.body)
        for string in self.stripped_comment(body):
            if is_string_valid(string):
                self.data.append(
                    Comment.create(comment, string, post_url, body)
                )
                break

    def stripped_comment(self, comment: object) -> str: return comment.strip().split(" ")

    def proccess_data(self):
        parsed_data = parse_comments(self.data)

        if len(parsed_data) == 0: 
            print("All comments allready registered.")
            return

        l = len(parsed_data)
        progressbar(0, l, f"Proccessing {l} objects: ")
        for i, obj in enumerate(parsed_data):

            result = API.get_stock(obj["symbol"])
            if result is None:
                company_name, exchange = get_stock_data(obj["symbol"])  
                if company_name is None: continue
                else: API.insert_stock(obj["symbol"], company_name, exchange)
            
            else: 
                company_name = result[0][0]
                exchange = result[0][1]

            try: scores = analyze(obj["comment_body"])
            except Exception as e:
                print(f"Sentiment analyzis error: {e}")
                continue
            
            API.insert_comment(
                obj["symbol"], 
                scores["neg"], 
                scores["neu"],
                scores["pos"],
                self.sub,
                obj["post_url"],
                obj["comment_url"],
                obj["comment_body"],
                obj["author"],
                obj["created_date"],
                obj["likes"]
                )

            progressbar(i + 1, l, None)
            
