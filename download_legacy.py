from legacy import Legacy
from db import GET
from util.progress_bar import progressbar

if __name__ == "__main__":
    symbols = GET.legacy_stocks()[:200]
    l = Legacy()

    progressbar(0, len(symbols), f"Fetching data from {len(symbols)} symbols: ")
    for i, symbol in enumerate(symbols): 
        l.run(symbol[0])
        progressbar(i + 1, len(symbols), None)

    l._insert()

    print("Updating symbols")
    for symbol in symbols: l._update(symbol[0])
    # progressbar(0, len(symbols), f"Inserting legacy data for {len(symbols)} symbols: ")
    # for i, symbol in enumerate(symbols):
    #     l.run(symbol[0])
    #     progressbar(i + 1, len(symbols), None)