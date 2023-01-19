import sys
from scrapers import Reddit


if __name__ == "__main__":
    b = Reddit(str(sys.argv[1]), int(sys.argv[2]))
    b.run()
    b.proccess_data()