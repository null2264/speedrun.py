import json


from aiohttp import ClientSession


from .errors import RateLimited
from .game import Game
from .page import Page
from .utils import urlify


from typing import Optional, Iterable


class SpeedrunPy:
    def __init__(self, session: Optional[ClientSession] = None) -> None:
        """
        Wrapper for speedrun.com's API
        """
        self._session: ClientSession = session
        self.base_url = "https://www.speedrun.com/api/v1"
        self.user_agent = "speedrun.py/0.0.1"

    async def close(self):
        await self._session.close()

    async def _generate_session(self):
        """|coro|

        Must be a coroutine to avoid the deprecation warning of Python 3.9+.
        """
        return ClientSession(headers={"User-Agent": self.user_agent})

    async def _request(self, query: str, *, endpoint: str, method: str = "get") -> dict:
        """|coro|

        Request data from speedrun.com api
        """
        # TODO: Move all request into `http.py`
        if self._session is None:
            self._session = await self._generate_session()

        action = getattr(self._session, method.lower(), self._session.get)
        async with action(self.base_url + endpoint + query) as res:
            if res.status == 420:
                raise RateLimited from None
            data = await res.json()
            return data

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

        data = await self._request(query, endpoint="/games")

        return Page(page_info=data["pagination"], data=data["data"], cls=Game, session=self._session)
