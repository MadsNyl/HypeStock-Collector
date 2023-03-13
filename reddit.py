import sys
from social_media import Reddit
from db import API, GET


def main():
    subs = GET.subreddits()
    subs = list(map(lambda x: x[0], subs))
    count = 5
    analyze = False

    if len(sys.argv) > 1: analyze = sys.argv[1].lower() == "true"
    if len(sys.argv) > 2: count = sys.argv[2] 

    b = Reddit(subs, count, analyze)
    b.run()

if __name__ == "__main__": main()
