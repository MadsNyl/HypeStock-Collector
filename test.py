import requests

res = requests.get("https://raw.githubusercontent.com/rreichel3/US-Stock-Symbols/main/amex/amex_full_tickers.json")
print(res.text)