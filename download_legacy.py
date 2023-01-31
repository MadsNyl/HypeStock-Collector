from legacy import Legacy
from db.controller import API
from functions.progress_bar import progressbar

symbols = API.get_legacy_stocks()
if __name__ == "__main__":
    l = Legacy()
    progressbar(0, len(symbols), f"Inserting legacy data for {len(symbols)} symbols: ")
    for i, symbol in enumerate(symbols):
        l.run(symbol[0])
        progressbar(i + 1, len(symbols), None)