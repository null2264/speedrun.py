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
from __future__ import annotations

import asyncio
from typing import ClassVar, Optional, Union

from aiohttp import ClientSession

from .errors import HTTPException
from .utils import json_or_text, urlify


class Route:

    BASE_URL: ClassVar[str] = "https://www.speedrun.com/api/v1"

    def __init__(self, method: str, path: str, **parameters: dict) -> None:
        self.method: str = method
        self.path: str = path
        url = self.BASE_URL + self.path
        if parameters:
            url += urlify(**parameters)
        self.url = url


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
        """
        Safely close session
        """
        if self._session:
            await self._session.close()

    async def request(self, route: Route, **kwargs) -> Union[dict, str]:
        """|coro|

        Request data from speedrun.com api
        """
        if self._session is None:
            self._session = await self._generate_session()

        for tries in range(5):
            async with self._session.request(
                route.method, route.url, **kwargs
            ) as response:
                data = await json_or_text(response)

                if 300 > response.status >= 200:
                    return data

                retry_after: float = 60.00

                if response.status == 420:
                    # Handles ratelimited
                    print("Rate limited, retrying in {} seconds".format(retry_after))
                    await asyncio.sleep(retry_after)
                    continue

        # ran out of tries
        raise HTTPException from None

    async def get_from_url(self, url: str) -> Optional[bytes]:
        async with self._session.get(url) as resp:  # type: ignore
            return await resp.read()

    def _games(
        self,
        *,
        name: Optional[str],
        abbreviation: Optional[str],
        released: Optional[int],
        gametype: Optional[str],
        platform: Optional[str],
        region: Optional[str],
        genre: Optional[str],
        engine: Optional[str],
        developer: Optional[str],
        publisher: Optional[str],
        moderator: Optional[str],
        romhack: Optional[str],
        _bulk: Optional[bool],
        offset: Optional[int],
        max: Optional[int],
    ):
        query = {}

        if name:
            query["name"] = name

        if abbreviation:
            query["abbreviation"] = abbreviation

        if released:
            query["released"] = released

        if gametype:
            query["gametype"] = gametype

        if platform:
            query["platform"] = platform

        if region:
            query["region"] = region

        if genre:
            query["genre"] = genre

        if engine:
            query["engine"] = engine

        if developer:
            query["developer"] = engine

        if publisher:
            query["publisher"] = publisher

        if moderator:
            query["moderator"] = moderator

        if romhack:
            query["romhack"] = romhack

        # if _bulk:
        #     query["_bulk"] = _bulk

        if offset:
            query["offset"] = offset

        if max:
            query["max"] = max

        if not _bulk:
            # Can't embed in _bulk mode
            query["embed"] = ",".join(
                (
                    "levels.variables",
                    "levels.categories.variables",
                    "categories.variables",
                    "moderators",
                    "gametypes",
                    "platforms",
                    "regions",
                    "genres",
                    "engines",
                    "developers",
                    "publishers",
                    "variables",
                )
            )
        else:
            query["_bulk"] = "True"

        route = Route("GET", "/games", **query)

        return self.request(route)

    def _users(
        self,
        *,
        lookup: Optional[str],
        name: Optional[str],
        twitch: Optional[str],
        hitbox: Optional[str],
        twitter: Optional[str],
        speedrunslive: Optional[str],
        offset: Optional[int],
        max: Optional[int],
    ):
        query = {}

        if lookup:
            query["lookup"] = lookup

        if name:
            query["name"] = name

        if twitch:
            query["twitch"] = twitch

        if hitbox:
            query["hitbox"] = hitbox

        if twitter:
            query["twitter"] = twitter

        if speedrunslive:
            query["speedrunslive"] = speedrunslive

        if offset:
            query["offset"] = offset

        if max:
            query["max"] = max

        route = Route("GET", "/users", **query)

        return self.request(route)
