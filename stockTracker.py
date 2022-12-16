# This class tracks occurrences of stocks mentioned in
# the subreddits

class Stock:

    _title: str
    _symbol: str
    _count: int = 1

    def __init__(self, title, symbol) -> None:
        self._title = title
        self._symbol = symbol

    def increment(self, x) -> None:
        self._count += x
    
    def decrement(self, x) -> None:
        self._count -= x
    
    def getCount(self) -> int:
        return self._count
    
    def getTitle(self) -> str:
        return self._title

    def getSymbol(self) -> str: 
        return self._symbol

    def __str__(self) -> str:
        return f"Stock Symbol: {self.getSymbol()} - Company Name: {self.getTitle()} - Stock Count: {self.getCount()}"
