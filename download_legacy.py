from legacy import Legacy
from db.controller import API
from functions.progress_bar import progressbar

if __name__ == "__main__":
    symbols = API.get_legacy_stocks()
    symbols = symbols[:10]
    l = Legacy()
    progressbar(0, len(symbols), f"Inserting legacy data for {len(symbols)} symbols: ")
    for i, symbol in enumerate(symbols):
        l.run(symbol[0])
        progressbar(i + 1, len(symbols), None)