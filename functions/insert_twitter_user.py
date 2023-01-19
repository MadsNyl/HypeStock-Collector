from db.db import DB
import sys

def insert(username: str, url: str) -> None:
    """
        Inserts twitter user into db.
    """
    db = DB
    db.insert_twitter_user(username, url)


insert(str(sys.argv[1]), str(sys.argv[2]))