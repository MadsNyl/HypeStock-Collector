from social_media.settings import reddit
from db import API, GET, INSERT  
from util.progress_bar import progressbar
from util.valid_symbol import is_string_valid
from util.get_stock_data import get_stock_data
from util.sentiment_analyzis import analyze
from util.validate_comment import parse_comments
from util.remove_emojies import remove_emojies
from models.comment import Comment
from datetime import datetime

class Reddit():

    # __subreddit: reddit.subreddit
    __limit: int
    __data: list[dict] = []
    __analyze: bool
    _comments: list[object] = []
    _tickers: dict[str: None]
    _comment_urls: dict[str: None]

    def __init__(self, subreddits: list[str], limit: int, analyze: bool) -> None:
        self.__subs = subreddits
        self.__limit = limit
        self.__analyze = analyze
        self._tickers = GET.tickers()
        self._comment_urls = GET.comment_urls()
    
    def run(self) -> None:
        self._collect_posts()
        self._process_comments()    

    def _collect_posts(self) -> None:
        progressbar(0, self.__limit, f"Collecting data from {len(self.__subs)} posts: ")

        for i, sub in enumerate(self.__subs):

            self._get_posts(sub)

            progressbar(i + 1, len(self.__subs), None)

    def _get_posts(self, sub: object) -> None:
        subreddit = reddit.subreddit(sub)
        for post in self._get_subreddit_posts(subreddit):
            post.comments.replace_more(limit=0)
            self._append_comments(post)

    def _get_subreddit_posts(self, subreddit: object) -> list: return subreddit.hot(limit=self.__limit)     

    def _append_comments(self, post: object) -> None:
        for comment in post.comments.list(): self._comments.append(comment)

    def _process_comments(self) -> None:
        progressbar(0, len(self._comments), f"\nProcessing {len(self._comments)} comments: ")
        for i, comment in enumerate(self._comments): 
            self._process_body(comment)
            progressbar(i + 1, len(self._comments), None)
    
    def _process_body(self, comment: object) -> None:
        body = remove_emojies(comment.body)
        for string in self.__stripped_comment(body):
            if string in self._tickers:
                self._insert_comment(comment, string)
                break
    
    def _insert_comment(self, comment: object, ticker: str) -> None:
        if comment.permalink in self._comment_urls: return

        try: scores = self.__get_sentiment_scores(remove_emojies(comment.body))
        except Exception as e:
            print(f"Sentiment analyzis error: {e}")
            return

        INSERT.comment(
            ticker, 
            scores["neg"], 
            scores["neu"],
            scores["pos"],
            comment.subreddit.display_name,
            comment.submission.permalink,
            comment.permalink,
            remove_emojies(comment.body),
            comment.author.name if comment.author else None,
            datetime.fromtimestamp(comment.created),
            comment.score
        )


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
            
