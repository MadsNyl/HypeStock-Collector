from social_media.settings import reddit
from db.controller import API 
from util.progress_bar import progressbar
from util.valid_symbol import is_string_valid
from util.get_stock_data import get_stock_data
from util.sentiment_analyzis import analyze
from util.validate_comment import parse_comments
from util.remove_emojies import remove_emojies
from models.comment import Comment

class Reddit():

    __subreddit: reddit.subreddit
    __limit: int
    __data: list[dict] = []
    __analyze: bool

    def __init__(self, subreddit: str, limit: int, analyze: bool) -> None:
        self.__subreddit = reddit.subreddit(subreddit)
        self.__sub = subreddit
        self.__limit = limit
        self.__analyze = analyze
    
    def run(self) -> None:

        progressbar(0, self.__limit, f"Collecting {self.__limit} subreddits: ")

        for i, sub in enumerate(self.__get_subreddits()):
            sub.comments.replace_more(limit=0)

            post_url = sub.permalink

            self.__process_comments(sub.comments.list(), post_url)

            progressbar(i + 1, self.__limit, None)       

    def __get_subreddits(self) -> list: return self.__subreddit.hot(limit=self.__limit)     

    def __process_comments(self, comments: list, post_url: str) -> None:
        for comment in comments: self.__process_body(comment, post_url)
    
    def __process_body(self, comment: object, post_url: str) -> None:
        body = remove_emojies(comment.body)
        for string in self.__stripped_comment(body):
            if is_string_valid(string):
                self.__data.append(
                    Comment.create(comment, string, post_url, body)
                )
                break

    def __stripped_comment(self, comment: object) -> str: return comment.strip().split(" ")

    def __get_sentiment_scores(self, text: str) -> dict[str:float]:
        if (self.__analyze): return analyze(text)
        return {
            "neg": None,
            "neu": None,
            "pos": None
        }

    def proccess_data(self):
        parsed_data = parse_comments(self.__data)

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
            
            try: scores = self.__get_sentiment_scores(obj["comment_body"])
            except Exception as e:
                print(f"Sentiment analyzis error: {e}")
                continue
            
            API.insert_comment(
                obj["symbol"], 
                scores["neg"], 
                scores["neu"],
                scores["pos"],
                self.__sub,
                obj["post_url"],
                obj["comment_url"],
                obj["comment_body"],
                obj["author"],
                obj["created_date"],
                obj["likes"]
                )

            progressbar(i + 1, l, None)
            
