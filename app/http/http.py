import asyncio
import requests

from requests import Response


class Http():

    def get(self, url: str, **kwargs) -> Response:
        return requests.get(url, **kwargs)


class AsyncHttp():

    async def get(self, url: str, **kwargs) -> Response:
        return await asyncio.to_thread(requests.get, url, **kwargs)


http = Http()
async_http = AsyncHttp