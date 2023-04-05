import requests

class Reddit():
    
    _URL: str = "https://api.pushshift.io/reddit/search/"
    _HEADERS = {'Accept': 'application/json'}

    def get_comments(self, subreddit: str, start: str, end: str, limit: int) -> dict:
        QUERY = f"{self._URL}comment/?subreddit={subreddit}&size={limit}&after={start}&before={end}"
        res = requests.get(QUERY, headers=self._HEADERS)
        json = res.json()
        return json["data"]      
