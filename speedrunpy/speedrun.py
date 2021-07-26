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
from typing import Optional, Iterable, List


from .errors import RateLimited
from .game import Game
from .http import HTTPClient
from .page import Page
from .user import User
from .utils import urlify


class SpeedrunPy:
    def __init__(
        self, session: Optional[ClientSession] = None, user_agent: Optional[str] = None
    ) -> None:
        """
        Wrapper for speedrun.com's API
        """
        user_agent = user_agent or "speedrun.py/0.0.1"
        self._http: HTTPClient = HTTPClient(session=session, user_agent=user_agent)

    async def close(self) -> None:
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
        data = await self._http._games(
            name=name,
            abbreviation=abbreviation,
            released=released,
            gametype=gametype,
            platform=platform,
            region=region,
            genre=genre,
            engine=engine,
            developer=developer,
            publisher=publisher,
            moderator=moderator,
            romhack=romhack,
            _bulk=_bulk,
            offset=offset,
            max=max,
            embeds=embeds,
        )

        games: List[Game] = [Game(i, http=self._http, embeds=embeds) for i in data["data"]]

        return Page(
            page_info=data["pagination"],
            data=games,
        )

    async def get_users(
        self,
        *,
        lookup: Optional[str] = None,
        name: Optional[str] = None,
        twitch: Optional[str] = None,
        hitbox: Optional[str] = None,
        twitter: Optional[str] = None,
        speedrunslive: Optional[str] = None,
        offset: Optional[int] = None,
        max: Optional[int] = None,
        embeds: Optional[Iterable] = None,
    ) -> Page:
        data = await self._http._users(
            lookup=lookup,
            name=name,
            twitch=twitch,
            hitbox=hitbox,
            twitter=twitter,
            speedrunslive=speedrunslive,
            offset=offset,
            max=max,
            embeds=embeds,
        )

        users = [User(i) for i in data["data"]]

        return Page(page_info=data["pagination"], data=users)
