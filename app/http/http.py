import asyncio
import requests

from requests import Response


class Http():

    async def get(self, url: str, asynchronous: bool = False, **kwargs) -> Response:
        if asynchronous:
            return await asyncio.to_thread(requests.get, url, **kwargs)

        return requests.get(url, **kwargs)
    


http = Http()