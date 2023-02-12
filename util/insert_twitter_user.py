from db import API
import sys

def insert(username: str, url: str) -> None:
    """
        Inserts twitter user into db.
    """
    API.insert_twitter_user(username, url)


insert(str(sys.argv[1]), str(sys.argv[2]))