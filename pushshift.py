import sys
from legacy import Reddit
from util import emoji_free_text, progressbar
from db import INSERT, GET


TICKERS = GET.tickers()
COMMENTS = GET.comment_urls()

def comments(sub: str, limit: int, start: int, end: int) -> None:
    l = Reddit()
    comments = l.get_comments(sub, f"{start}d", f"{end}d", limit)
    progressbar(0, limit, f"\nProcessing {limit} comments for {sub} from start {start}d to end {end}d: ")
    for i, comment in enumerate(comments): 
        if comment["permalink"] in COMMENTS: continue
        process_body(comment, sub)
        progressbar(i + 1, limit, None)

def process_body(comment: dict, subreddit: str) -> None:
    body = emoji_free_text(comment["body"])
    post_url = comment["permalink"].split("/")
    for word in body.strip().split(" "):
        if word in TICKERS:
            INSERT.comment(
                symbol=word,
                neg_score=None,
                neu_score=None,
                pos_score=None,
                subreddit=subreddit,
                post_url="/".join(post_url[:-2]),
                permalink=comment["permalink"],
                body=body,
                author=comment["author"],
                created_date=comment["utc_datetime_str"],
                likes=comment["score"]
            )
            return


def main():
    subs = GET.subreddits()
    subs = list(map(lambda x: x[0], subs))
    count = 500
    days = 300

    if len(sys.argv) > 1: count = sys.argv[1] 

    for sub in subs: 
        while days > 2: 
            comments(sub, count, days, days - 1) 
            days -= 1
        days = 300

if __name__ == "__main__": main()