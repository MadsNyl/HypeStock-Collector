from legacy.settings import DOWNLOAD_API, DOWNLOAD_PERIOD, USER_AGENT
from db.controller import API
import requests, os

class Legacy():
    
    __data: list[str] = []
    
    def run(self, symbol: str) -> None:
        self.__proccess(symbol)

    def __proccess(self, symbol: str) -> None:
        file = self.__download(symbol)
        self.__append_data(file, symbol)
        self.__delete_file(file)
        self.__insert()
        self.__update(symbol)
    
    def __insert(self) -> None: API.insert_trackings(self.__data)

    def __update(self, symbol: str) -> None: API.update_legacy(symbol)

    def __append_data(self, file: str, symbol: str) -> None:
        with open(file, "r") as f:
            next(f)
            for line in f:
                data = self.__split_line(line)
                if not self.__validate(data): continue
                self.__data.append((
                    symbol,
                    float(data[4]) if not self.__is_null(data[4]) else None,
                    float(data[3]) if not self.__is_null(data[3]) else None,
                    float(data[2]) if not self.__is_null(data[2]) else None,
                    int(data[6]) if not self.__is_null(data[6]) else None,
                    data[0],
                    None,
                    None
                ))

    def __validate(self, data: list[str]) -> bool:
        data = data[1:]
        return not all(self.__is_null(col) for col in data)

    def __is_null(self, data: str) -> bool: return data == "null" 

    def __delete_file(self, file: str) -> None: os.remove(file)  

    def __split_line(self, line: str) -> str: return line.strip().split(",")

    def __download(self, symbol: str) -> str:
        file = f"legacy/downloads/{symbol}.csv"
        headers = {"User-Agent": USER_AGENT}
        res = requests.get(f"{DOWNLOAD_API}{symbol}{DOWNLOAD_PERIOD}", headers=headers)
        open(file, "wb").write(res.content)
        return file