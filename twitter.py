from scrapers.twitter import Twitter
import sys

if __name__ == "__main__":
    t = Twitter(str(sys.argv[1]), int(sys.argv[2]))
    t.run()
    t.process_data()