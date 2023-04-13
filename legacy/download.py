from legacy.settings import DOWNLOAD_API, DOWNLOAD_PERIOD, USER_AGENT
from db import INSERT, UPDATE
from util import progressbar
import requests, os, datetime, time

class Legacy():
    
    _data: list[str] = []
    
    def run(self, symbol: str) -> None:
        self._proccess(symbol)

    def _proccess(self, symbol: str) -> None:
        file = self._download(symbol)
        self._append_data(file, symbol)
        self._delete_file(file)
        # self._insert()
        # self._update(symbol)
    
    def _insert(self) -> None: 
        progressbar(0, len(self._data), f"\nInserting {len(self._data)} trackings: ")
        for i, data in enumerate(self._data):

            if i > 0: self._insert_weekends(data, prev)

            INSERT.legacy(
                data[0],
                data[1],
                data[2],
                None,
                None,
                data[3]
            )
            prev = data

            progressbar(i + 1, len(self._data), None)

    def _insert_weekends(self, data: list, prev: list) -> None:
        prev_timing = prev[3]
        new_timing = data[3]
        prev_date = datetime.datetime.strptime(prev_timing, "%Y-%m-%d").date()
        new_date = datetime.datetime.strptime(new_timing, "%Y-%m-%d").date()

        diff_days = (new_date - prev_date).days
        if diff_days < 2: return

        for day in range(diff_days - 1):
            timing = prev_date + datetime.timedelta(days=day + 1)
            INSERT.legacy(
                prev[0],
                prev[1],
                prev[2],
                None,
                None,
                timing
            )

    def _update(self, symbol: str) -> None: UPDATE.legacy(symbol)

    def _append_data(self, file: str, symbol: str) -> None:
        with open(file, "r") as f:
            next(f)
            for line in f:
                data = self._split_line(line)
                if not self._validate(data): continue
                self._data.append((
                    symbol,
                    float(data[4]) if not self._is_null(data[4]) else None,
                    int(data[6]) if not self._is_null(data[6]) else None,
                    data[0]
                ))

    def _validate(self, data: list[str]) -> bool:
        data = data[1:]
        return not all(self._is_null(col) for col in data)

    def _is_null(self, data: str) -> bool: return data == "null" 

    def _delete_file(self, file: str) -> None: os.remove(file)  

    def _split_line(self, line: str) -> str: return line.strip().split(",")

    def _download(self, symbol: str) -> str:
        symbol = symbol.replace("/", "_")
        file = f"legacy/{symbol}.csv"
        headers = {"User-Agent": USER_AGENT}
        start = str(time.mktime(datetime.datetime(2020, 1, 1).timetuple())).split(".")[0]
        now = str(time.time()).split(".")[0]
        period = f"?period1={start}&period2={now}&interval=1d&events=history&includeAdjustedClose=true"
        res = requests.get(f"{DOWNLOAD_API}{symbol}{period}", headers=headers)
        open(file, "wb").write(res.content)
        return file