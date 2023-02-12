from update.settings import SYMBOL_LOOKUP_API
from util.progress_bar import progressbar
from db.controller import API
import requests, re

class Tracker():

    stocks: list = API.get_stocks()
    data: list = []

    def run(self) -> None:
        self.parse_data()
        if len(self.data) == 0: 
            print("No trackings to update.")
            return
        
        API.insert_trackings(self.data)

    def parse_data(self) -> None:
        progressbar(0, len(self.stocks), f"Gathering information of {len(self.stocks)} stocks: ")
        for i, stock in enumerate(self.stocks):
            symbol = stock[0]
            try: data = self.get_data(symbol)
            except Exception as e:
                print(e)
                continue
            if data is None: continue
            self.append(symbol, data)
            progressbar(i + 1, len(self.stocks), None)


    def append(self, symbol: str, data: dict) -> None:
        timing = self.format_timing(data["timing"])
        change = self.format_change(data["change"])
        change_pct = self.format_change_pct(data["change_pct"])

        if self.validate_timing(symbol, timing):
            self.data.append((
                symbol,
                self.format_price(data["last_price"]),
                self.format_price(data["min_price"]),
                self.format_price(data["max_price"]),
                self.format_volume(data["volume"]),
                timing,
                change,
                change_pct
            ))
    
    def validate_timing(self, symbol: str, timing: str) -> bool:
        pattern = re.compile("[0-9]{4}-[0-9]{2}-[0-9]{2}")
        if not pattern.match(timing): return False
        t = API.get_tracking(symbol)
        if not t: return True
        if str(timing) != str(t[0])[:10]: return True
        return False
    
    def format_volume(self, volume: str) -> int: return int(volume.replace(",", ""))

    def format_price(self, price: str) -> float: return float(price.replace(",", "")[1:])

    def format_change_pct(self, change_pct: str) -> float: 
        temp = change_pct.split(">")[1].split("<")[0][1:-2]
        temp = temp.replace(",", "")
        return float(temp)

    def format_change(self, change: str) -> float: 
        temp = change.split(">")[1].split("<")[0][1:]
        temp = temp.replace(",", "")
        return float(temp)

    def format_timing(self, timing: str) -> str:
        timing = timing[-10:]
        return f"{timing[-4:]}-{timing[-10:-8]}-{timing[-7:-5]}"

    def get_data(self, symbol: str):
        result = requests.get(SYMBOL_LOOKUP_API + symbol)
        json = result.json()

        if json["isValidSymbol"]: 
            return {
                "last_price": json["quote"]["lastPrice"],
                "min_price": json["quote"]["daysRangeMin"],
                "max_price": json["quote"]["daysRangeMax"],
                "volume": json["quote"]["todaysVolume"],
                "timing": json["quote"]["timing"],
                "change": json["quote"]["todaysChange"],
                "change_pct": json["quote"]["todaysChangePct"]
            }

        return None