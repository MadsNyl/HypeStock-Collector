from legacy import Legacy
from db.controller import API

symbols = API.get_stocks()

if __name__ == "__main__":
    l = Legacy()
    for symbol in symbols:
        l.run(symbol[0])