import asyncio

from app.http import http, build_url
from settings import API_URL


async def main():
    url = build_url(
        f"{API_URL}article",
        ["url_only=true"]
    )
    response = await http.get(url)
    print(response.json())

asyncio.run(main())