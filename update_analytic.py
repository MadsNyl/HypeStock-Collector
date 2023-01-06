from db import DB
import requests
from settings.credentials import SYMBOL_LOOKUP_API


def get_company_name(symbol):
    """
        Sends a request to schwab.com to check up stock symbol for company name.
    """
    result = requests.get(SYMBOL_LOOKUP_API + symbol)
    json = result.json()

    if json["isValidSymbol"]: 
        return json["companyInfo"]["companyName"], json["quote"]["lastPrice"], json["quote"]["daysRangeMin"], json["quote"]["daysRangeMax"], json["quote"]["todaysVolume"], json["quote"]["timing"], json["quote"]["todaysChange"], json["quote"]["todaysChangePct"] 

    return None, None, None, None, None, None, None, None

def check_date(timing, symbol):
    t = d.get_analytic(symbol)
    if not t: return False
    if str(timing) != str(t[0]): return True
    return False
        
d = DB()
analytics = d.get_all_stocks()
data = []
seen_stocks = []

print(len(analytics))
for analytic in analytics:
    if analytic[0] in seen_stocks: continue
    _, last_price, min_price, max_price, volume, timing, change, change_pct = get_company_name(analytic[0])
    if not timing: continue
    timing = timing[-10:]
    timing = f"{timing[-4:]}-{timing[-10:-8]}-{timing[-7:-5]}"
    change = change.split(">")[1].split("<")[0][1:]
    change_pct = change_pct.split(">")[1].split("<")[0][1:-2]
    date_check = check_date(timing, analytic[0])
    if date_check:
        data.append((analytic[0], float(last_price.replace(",", "")[1:]), float(min_price.replace(",", "")[1:]), float(max_price.replace(",", "")[1:]), int(volume.replace(",", "")), timing, float(change.replace(",", "")), float(change_pct.replace(",", ""))))
        seen_stocks.append(analytic[0])

print("starts updating")


if len(data) == 0: print("Nothing to update.")
else: d.update_analytics(data)
