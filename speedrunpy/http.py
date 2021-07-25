"""
MIT License

Copyright (c) 2021-Present null2264

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""


from aiohttp import ClientSession
from typing import Optional


BASE_URL = "https://www.speedrun.com/api/v1"


class HTTPClient:
    def __init__(self, *, session: Optional[ClientSession] = None, user_agent: str):
        self._session = session
        self.user_agent = user_agent

    async def _generate_session(self) -> ClientSession:
        """|coro|

        Must be a coroutine to avoid the deprecation warning of Python 3.9+.
        """
        return ClientSession(headers={"User-Agent": self.user_agent})

    async def close(self) -> None:
        await self._session.close()

    async def _request(self, query: str, *, endpoint: str, method: str = "get") -> dict:
        """|coro|

        Request data from speedrun.com api
        """
        # TODO: Move all request into `http.py`
        if self._session is None:
            self._session = await self._generate_session()

        action = getattr(self._session, method.lower(), self._session.get)
        async with action(BASE_URL + endpoint + query) as res:
            if res.status == 420:
                raise RateLimited from None
            data = await res.json()
            return data
