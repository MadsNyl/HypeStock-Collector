from twitter_user import TwitterUser
import sys

usernames = [
    "Stockwits",
    "Jake__Wujastyk",
    "howardlindzon"
]   

if __name__ == "__main__":
    t = TwitterUser(usernames, int(sys.argv[1]))
    t.run()
    t.process_data()