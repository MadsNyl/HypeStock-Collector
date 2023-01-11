from settings.credentials import twitter
import tweepy


response = tweepy.Paginator(twitter.search_recent_tweets, query="stocks", max_results=10, tweet_fields=["author_id", "created_at", "text", "public_metrics", "source"], user_fields=["name", "username"]).flatten(limit=10)

for tweet in response:
    print(tweet.public_metrics)
    break