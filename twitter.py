import snscrape.modules.twitter as sntwitter
from settings.credentials import SYMBOL_LOOKUP_API
from db import DB
from stockTracker import Stock
from nltk.sentiment import SentimentIntensityAnalyzer
from functions.progress_bar import print_progress_bar, print_progress_bar_objects, print_progress_bar_tweets
import requests, nltk


tweets = sntwitter.TwitterHashtagScraper("stocks").get_items()


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
        self.seen_stocks = self.db.update_record()
        nltk.download("vader-lexicon")
        self.sia = SentimentIntensityAnalyzer()

    
    def run(self) -> None:
        self.collect_tweets()

    def collect_tweets(self) -> None:
        # l = len(self.tweets)
        
        # print_progress_bar_tweets(l)
        for i, tweet in enumerate(self.tweets):
            if i > self.limit: break
            
            self.data.append(tweet)
            # print_progress_bar(i + 1, l, prefix="Progress", suffix="Complete")
    
    def process_data(self) -> None:
        l = len(self.data)
        
        print_progress_bar_objects(l)
        for i, tweet in enumerate(self.data):
            self.process_content(tweet)
            print_progress_bar(i + 1, l, prefix="Progress", suffix="Complete")
    
    def process_content(self, tweet: object) -> None:
        for string in tweet.content.strip().split(" "):
            if not self.is_stock_string_valid(string): continue

            # check if symbol exsist and get info
            company_name, last_price, min_price, max_price, volume, timing = self.get_company_name(string)  

            if not company_name: continue

            # get sentiment score of content text
            sentiment_score = self.analyze(tweet.content)

            # insert stock in db
            self.insert_stock(string, company_name)

            # check author
            if tweet.user: author = tweet.user.username

            # insert sentiment in db
            self.db.insert_sentiment(string, sentiment_score, False, tweet.id, tweet.id, tweet.content, author) 

            # insert tracking in db
            self.insert_tracking(string, last_price, min_price, max_price, volume, timing)

            break
                
    def insert_tracking(self, symbol: str, last_price: str, min_price: str, max_price: str, volume: str, timing: str) -> None:
        result = self.db.get_todays_tracking(symbol)

        if result: return

        timing = timing[-10:]
        timing = f"{timing[-4:]}-{timing[-10:-8]}-{timing[-7:-5]}"
        self.db.insert_tracking(symbol, last_price, min_price, max_price, volume, timing)


    def is_stock_string_valid(self, string: str) -> bool:
        if string.startswith("$"): string = string[1:]
        return 5 >= len(string) >= 2 and string[0].isupper() and string[len(string) - 1].isupper()


    def insert_stock(self, symbol: str, company_name: str) -> None:
        if symbol in self.seen_stocks: self.db.update_stock(self.seen_stocks[symbol])
        else:
            stock = Stock(company_name, symbol)
            self.db.insert_stock(stock)
            self.seen_stocks[symbol] = stock
    
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