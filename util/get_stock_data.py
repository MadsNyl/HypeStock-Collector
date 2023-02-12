import requests
from util.settings import SYMBOL_LOOKUP_API

def get_stock_data(symbol: str):
    """
        Sends a request to stock api to check up stock symbol for data.
    """
    try:
        # get json data
        result = requests.get(SYMBOL_LOOKUP_API + symbol)
        json = result.json()

        if json["isValidSymbol"]: 
            return json["companyInfo"]["companyName"], json["companyInfo"]["exchange"] 

        return None, None
    except Exception as e:
        print(e)
        return None, None