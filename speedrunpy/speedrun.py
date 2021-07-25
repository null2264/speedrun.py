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


import json


from aiohttp import ClientSession
from typing import Optional, Iterable


from .errors import RateLimited
from .game import Game
from .http import HTTPClient
from .page import Page
from .utils import urlify


class SpeedrunPy:
    def __init__(self, session: Optional[ClientSession] = None) -> None:
        """
        Wrapper for speedrun.com's API
        """
        user_agent = "speedrun.py/0.0.1"
        self._http: HTTPClient = HTTPClient(session=session, user_agent=user_agent)

    async def close(self):
        await self._http.close()

    async def get_games(
        self,
        *,
        name: Optional[str] = None,
        abbreviation: Optional[str] = None,
        released: Optional[int] = None,
        gametype: Optional[str] = None,
        platform: Optional[str] = None,
        region: Optional[str] = None,
        genre: Optional[str] = None,
        engine: Optional[str] = None,
        developer: Optional[str] = None,
        publisher: Optional[str] = None,
        moderator: Optional[str] = None,
        romhack: Optional[str] = None,
        _bulk: Optional[str] = None,
        offset: Optional[int] = None,
        max: Optional[int] = None,
        embeds: Optional[Iterable] = None,
    ) -> Page:
        """|coro|

        Get games data
        """
        params = {
            "name": name,
            "abbreviation": abbreviation,
            "released": released,
            "gametype": gametype,
            "platform": platform,
            "region": region,
            "genre": genre,
            "engine": engine,
            "developer": developer,
            "publisher": publisher,
            "moderator": moderator,
            "romhack": romhack,
            "_bulk": _bulk,
            "offset": offset,
            "max": max,
            "embeds": ",".join(embeds or []),
        }
        query = urlify(**params)

        data = await self._http._request(query, endpoint="/games")

        return Page(
            page_info=data["pagination"],
            data=data["data"],
            cls=Game,
            http=self._http,
        )
