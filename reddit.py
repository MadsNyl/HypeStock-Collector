import sys
from scrapers import Reddit
from db import API


if __name__ == "__main__":

    subs = API.get_subreddits()
    subs = list(map(lambda x: x[0], subs))

    for sub in subs:
        print(f"\nCollecting from {sub}:\n")
        b = Reddit(sub, 15, sys.argv[1].lower() == "true")
        b.run()
        b.proccess_data()