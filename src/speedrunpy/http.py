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
import sys
from typing import (
    TYPE_CHECKING,
    Any,
    ClassVar,
    Coroutine,
    Dict,
    Optional,
    TypeVar,
    Union,
)

import aiohttp
from aiohttp import ClientResponse, ClientSession

from . import __version__
from .embeds import EMBED_GAMES, EMBED_LEADERBOARDS, EMBED_RUNS, FULL_EMBED_LEADERBOARDS
from .errors import HTTPException
from .utils import from_json, urlify


if TYPE_CHECKING:
    from .models.types import SpeedrunPagedResponse, SpeedrunResponse, GetUserSummaryResponse

    T = TypeVar("T")
    Response = Coroutine[Any, Any, T]


async def json_or_text(response: ClientResponse) -> Union[Dict[str, Any], str]:
    text = await response.text(encoding="utf-8")
    try:
        if response.headers["content-type"] == "application/json":
            return from_json(text)
    except KeyError:
        pass

    return text


class Route:
    BASE_URL: ClassVar[str] = "https://www.speedrun.com/api"

    def __init__(self, method: str, api_version: int, path: str, **parameters: Dict[str, Any]) -> None:
        self.method: str = method
        self.path: str = path
        self.api_version: int = api_version
        self.parameters: Dict[str, Any] = parameters

    @property
    def url(self) -> str:
        url = self.BASE_URL + f"/v{self.api_version}" + self.path
        if self.parameters:
            url += urlify(**self.parameters)
        return url


class HTTPClient:
    def __init__(
        self,
        *,
        user_agent: Optional[str],
        token: Optional[str] = None,
        session: Optional[ClientSession] = None,
    ):
        self.token: Optional[str] = token
        self._authenticated: bool = self.token is not None
        self._session: Optional[ClientSession] = session
        _user_agent = "speedrun.py (https://github.com/null2264/speedrun.py {0}) Python/{1[0]}.{1[1]} aiohttp/{2}"
        self.user_agent: str = user_agent or _user_agent.format(__version__, sys.version_info, aiohttp.__version__)

    async def _generate_session(self) -> ClientSession:
        """|coro|

        Must be a coroutine to avoid the deprecation warning of Python 3.9+.
        """
        headers = {"User-Agent": self.user_agent}
        if self.token:
            headers["X-API-Key"] = self.token

        return ClientSession(headers=headers)

    async def close(self) -> None:
        """
        Safely close session
        """
        if self._session:
            await self._session.close()

    async def request(self, route: Route, **kwargs: Dict[str, Any]) -> Any:
        """|coro|

        Request data from speedrun.com api
        """
        if self._session is None:
            self._session = await self._generate_session()

        for _ in range(5):  # 5 tries
            async with self._session.request(route.method, route.url, **kwargs) as response:
                data = await json_or_text(response)

                if 300 > response.status >= 200:
                    return data

                retry_after: float = 60.00

                if response.status == 420 or response.status == 429:
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
    ) -> Response[SpeedrunPagedResponse]:
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

        if offset:
            query["offset"] = offset

        if max:
            query["max"] = max

        if not _bulk:
            # Can't embed in _bulk mode
            query["embed"] = ",".join(EMBED_GAMES)

        query["_bulk"] = str(_bulk)

        route = Route("GET", 1, "/games", **query)

        return self.request(route)

    def _game_by_id(self, *, id: str) -> Response[SpeedrunResponse]:
        query: Dict[str, Any] = {"embed": ",".join(EMBED_GAMES)}

        route = Route("GET", 1, f"/games/{id}", **query)

        return self.request(route)

    def _derived_games(
        self,
        base_game_id: str,
        /,
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
        _bulk: Optional[bool],
        offset: Optional[int],
        max: Optional[int],
    ) -> Response[SpeedrunPagedResponse]:
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

        if offset:
            query["offset"] = offset

        if max:
            query["max"] = max

        if not _bulk:
            # Can't embed in _bulk mode
            query["embed"] = ",".join(EMBED_GAMES)

        query["_bulk"] = str(_bulk)

        route = Route("GET", 1, f"/games/{base_game_id}/derived-games", **query)

        return self.request(route)

    def _game_records(self, game_id):
        pass

    def _category_variables(self, category_id):
        route = Route("GET", 1, f"/categories/{category_id}/variables")

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
    ) -> Response[SpeedrunPagedResponse]:
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

        route = Route("GET", 1, "/users", **query)

        return self.request(route)

    def _user_by_id(self, id: str) -> Response[SpeedrunResponse]:
        route = Route("GET", 1, f"/users/{id}")

        return self.request(route)

    def _get_user_summary(self, url: str) -> Response[GetUserSummaryResponse]:
        query = {}

        query["url"] = url

        route = Route("GET", 2, "/GetUserSummary", **query)

        return self.request(route)

    def _user_personal_bests(self, id: str) -> Response[SpeedrunResponse]:
        query = {}

        query["embed"] = ",".join(EMBED_RUNS)

        route = Route("GET", 1, f"/users/{id}/personal-bests", **query)

        return self.request(route)

    def _profile(self) -> Response[SpeedrunResponse]:
        route = Route("GET", 1, "/profile")

        return self.request(route)

    def _runs(
        self,
        *,
        user: Optional[str],
        guest: Optional[str],
        examiner: Optional[str],
        game: Optional[str],
        level: Optional[str],
        category: Optional[str],
        region: Optional[str],
        emulated: Optional[bool],
        status: Optional[str],
    ) -> Response[SpeedrunPagedResponse]:
        query = {}

        if user:
            query["user"] = user

        if guest:
            query["guest"] = guest

        if examiner:
            query["examiner"] = examiner

        if game:
            query["game"] = game

        if level:
            query["level"] = level

        if category:
            query["category"] = category

        if region:
            query["region"] = region

        if emulated is not None:
            query["emulated"] = int(emulated)

        if status:
            query["status"] = status

        query["embed"] = ",".join(EMBED_RUNS)

        route = Route("GET", 1, "/runs", **query)

        return self.request(route)

    def _run_by_id(self, id: str) -> Response[SpeedrunResponse]:
        query = {}

        query["embed"] = ",".join(EMBED_RUNS)

        route = Route("GET", 1, f"/runs/{id}", **query)

        return self.request(route)
