class Stock:

    _title: str
    _symbol: str
    _exchange: str

    def __init__(self, title: str, symbol: str, exchange: str) -> None:
        self._title = title
        self._symbol = symbol
        self._exchange = exchange
    
    def getTitle(self) -> str:
        return self._title
    
    def getExchange(self) -> str:
        return self._exchange

    def getSymbol(self) -> str: 
        return self._symbol

    def __str__(self) -> str:
        return f"Stock Symbol: {self._symbol} - Company Name: {self._title} - Exchange: {self._exchange}"
