import sys
from social_media import Reddit
from db import API


def main():
    subs = API.get_subreddits()
    subs = list(map(lambda x: x[0], subs))
    count = 5
    if len(sys.argv) > 2: count = sys.argv[2] 

    for sub in subs:
        print(f"\nCollecting from {sub}:\n")
        b = Reddit(sub, count, sys.argv[1].lower() == "true")
        b.run()
        b.proccess_data()

if __name__ == "__main__": main()
