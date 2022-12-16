from settings.credentials import reddit, SYMBOL_LOOKUP_API
from stockTracker import Stock
from db import DB
from nltk.sentiment import SentimentIntensityAnalyzer
from functions.progress_bar import print_progress_bar, print_progress_bar_subs, print_progress_bar_objects
import requests, nltk

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
            print_progress_bar(i + 1, self.limit, prefix="Progress: ", suffix="Complete")            

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
            if self.is_stock_string_valid(string):
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


    def is_stock_string_valid(self, string: str) -> bool:
        return 5 >= len(string) >= 2 and string[0].isupper() and string[len(string) - 1].isupper()

    def proccess_data(self):
        l = len(self.data)
        print_progress_bar_objects(l)
        for i, obj in enumerate(self.data):
            company_name, last_price, min_price, max_price, volume, timing = self.get_company_name(obj["symbol"])  
            if company_name is None: continue

            # get sentiment score of comment text
            sentiment_score = self.analyze(obj["comment_body"])

            # insert stock to db
            self.insert_stock(company_name, obj["symbol"])
            
            # insert sentiment to db
            self.db.insert_sentiment(obj["symbol"], sentiment_score, True, obj["post_url"], obj["comment_url"], obj["comment_body"], obj["author"])

            # insert tracking to db
            self.insert_tracking(obj["symbol"], last_price, min_price, max_price, volume, timing)

            # update progress bar
            print_progress_bar(i + 1, l, prefix="Progress", suffix="Complete")
    
    def insert_stock(self, company_name: str, symbol: str) -> None:
        if symbol in self.seen_stocks: 
            self.seen_stocks[symbol].increment(1)
            self.db.update_stock(self.seen_stocks[symbol])
        else:
            stock = Stock(company_name, symbol)
            self.db.insert_stock(stock)
            self.seen_stocks[symbol] = stock

    def insert_tracking(self, symbol, last_price, min_price, max_price, volume, timing):
        result = self.db.get_todays_tracking(symbol)

        # if stock already registered in analytics, return
        if result: return
            # if (str(result[0]) == str(date.today())): return
        
        timing = timing[-10:]
        timing = f"{timing[-4:]}-{timing[-10:-8]}-{timing[-7:-5]}"
        self.db.insert_tracking(symbol, last_price, min_price, max_price, volume, timing)


    def get_company_name(self, symbol):
        """
            Sends a request to schwab.com to check up stock symbol for company name.
        """
        try:
            result = requests.get(SYMBOL_LOOKUP_API + symbol)
            json = result.json()

            if json["isValidSymbol"]: 
                return json["companyInfo"]["companyName"], json["quote"]["lastPrice"], json["quote"]["daysRangeMin"], json["quote"]["daysRangeMax"], json["quote"]["todaysVolume"], json["quote"]["timing"] 

            return None, None, None, None, None, None 
        except Exception as e:
            print(e)
            return None, None, None, None, None, None 
    
    def analyze(self, text):
        results = self.sia.polarity_scores(text)
        return results["compound"]     

