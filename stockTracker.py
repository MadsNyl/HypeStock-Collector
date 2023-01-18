# This class tracks occurrences of stocks mentioned in
# the subreddits

class Stock:

    _title: str
    _symbol: str
    _count: int = 1
    _exchange: str

    def __init__(self, title: str, symbol: str, exchange: str) -> None:
        self._title = title
        self._symbol = symbol
        self._exchange = exchange

    def increment(self, x) -> None:
        self._count += x
    
    def decrement(self, x) -> None:
        self._count -= x
    
    def getCount(self) -> int:
        return self._count
    
    def getTitle(self) -> str:
        return self._title
    
    def getExchange(self) -> str:
        return self._exchange

    def getSymbol(self) -> str: 
        return self._symbol

    def __str__(self) -> str:
        return f"Stock Symbol: {self.getSymbol()} - Company Name: {self.getTitle()} - Stock Count: {self.getCount()}"
