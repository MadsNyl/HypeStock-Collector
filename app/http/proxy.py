import requests
from settings import PROXIES
from random import choice


class Proxy():
    _proxies: list[str] = []
    _PROXIES_URL: str = PROXIES
    _current_index: int = 0

    def __init__(self) -> None:
        self._get_proxies()

    def __iter__(self) -> list[str]:
        return self._proxies

    def __len__(self) -> int:
        return len(self._proxies)

    def __getitem__(self, index) -> str:
        return self._proxies[index]

    @property
    def proxy(self) -> str | None:
        if not len(self._proxies): return None
        return choice(self._proxies)

    def next(self) -> None:
        if not len(self._proxies):
            return

        if self._current_index == len(self._proxies) - 1:
            self._current_index = 0
        else:
            self._current_index += 1

    def _get_proxies(self) -> None:
        response = requests.get(self._PROXIES_URL)

        if response.status_code != 200:
            return

        self._proxies = response.text.split("\n")
