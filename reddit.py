import sys
from social_media import Reddit
from db import GET


def main():
    subs = GET.subreddits()
    subs = list(map(lambda x: x[0], subs))
    count = 5

    if len(sys.argv) > 1: count = sys.argv[1] 

    b = Reddit(subs, count)
    b.run()

if __name__ == "__main__": main()
