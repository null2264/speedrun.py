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

from typing import List, Optional, Union

from aiohttp import ClientSession

from .errors import HTTPException, NoDataFound
from .http import HTTPClient
from .models.game import Game, PartialGame
from .models.page import Page
from .models.run import Run
from .models.user import User


class Client:
    def __init__(
        self,
        session: Optional[ClientSession] = None,
        user_agent: Optional[str] = None,
        token: Optional[str] = None,
    ) -> None:
        """
        Wrapper for speedrun.com's API
        """
        self._http: HTTPClient = HTTPClient(
            session=session,
            user_agent=user_agent,
            token=token,
        )

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
        _bulk: bool = False,
        offset: Optional[int] = None,
        max: Optional[int] = None,
        error_on_empty: bool = True,
    ) -> Page[Union[PartialGame, Game]]:
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
        )

        cls = PartialGame if _bulk else Game

        games: List[PartialGame] = [cls(i, http=self._http) for i in data["data"]]

        if error_on_empty and not games:
            raise NoDataFound

        return Page(
            page_info=data["pagination"],
            data=games,
        )

    async def get_game_by_id(self, *, id: str) -> Game:
        """Get a game data by its ID or Abbreviation"""
        data = await self._http._game_by_id(id=id)

        return Game(data["data"], http=self._http)

    async def get_derived_games_by_id(
        self,
        *,
        id: str,
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
        _bulk: bool = False,
        offset: Optional[int] = None,
        max: Optional[int] = None,
        error_on_empty: bool = True,
    ) -> Page[Union[PartialGame, Game]]:
        data = await self._http._derived_games(
            id,
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
            _bulk=_bulk,
            offset=offset,
            max=max,
        )

        cls = PartialGame if _bulk else Game

        games: List[PartialGame] = [cls(i, http=self._http) for i in data["data"]]

        if error_on_empty and not games:
            raise NoDataFound

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
        error_on_empty: bool = True,
    ) -> Page[User]:
        data = await self._http._users(
            lookup=lookup,
            name=name,
            twitch=twitch,
            hitbox=hitbox,
            twitter=twitter,
            speedrunslive=speedrunslive,
            offset=offset,
            max=max,
        )

        users = [User(i, http=self._http) for i in data["data"]]

        if error_on_empty and not users:
            raise NoDataFound

        return Page(page_info=data["pagination"], data=users)

    async def get_user_by_id(self, *, id, error_on_empty: bool = True) -> Union[User, None]:
        data = await self._http._user_by_id(id)

        if not data["data"]:
            if error_on_empty:
                raise NoDataFound
            return None

        return User(data["data"], http=self._http)

    async def get_user_summary(self, *, url) -> User:
        data = await self._http._get_user_summary(url)

        if data.get("error"):
            raise HTTPException

        return User(data, http=self._http)

    async def find_user(self, query: str, *, error_on_empty: bool = True) -> Union[User, None]:
        try:
            initial_data = await self.get_users(lookup=query)
            return initial_data[0]
        except NoDataFound:
            return await self.get_user_by_id(id=query, error_on_empty=error_on_empty)

    async def get_profile(
        self,
        *,
        error_on_empty: bool = True,
    ) -> User | None:
        data = await self._http._profile()

        if not data["data"]:
            if error_on_empty:
                raise NoDataFound
            return None

        return User(data["data"], http=self._http)

    async def get_runs(
        self,
        *,
        user: Optional[str] = None,
        guest: Optional[str] = None,
        examiner: Optional[str] = None,
        game: Optional[str] = None,
        level: Optional[str] = None,
        category: Optional[str] = None,
        region: Optional[str] = None,
        emulated: Optional[bool] = None,
        status: Optional[str] = None,
        error_on_empty: bool = True,
    ) -> Page[Run]:
        data = await self._http._runs(
            user=user,
            guest=guest,
            examiner=examiner,
            game=game,
            level=level,
            category=category,
            region=region,
            emulated=emulated,
            status=status,
        )

        runs = [Run(i, http=self._http) for i in data["data"]]

        if error_on_empty and not runs:
            raise NoDataFound

        return Page(page_info=data["pagination"], data=runs)

    async def get_run_by_id(
        self,
        *,
        id: str,
        error_on_empty: bool = True,
    ) -> Union[Run, None]:
        data = await self._http._run_by_id(id)

        if not data["data"]:
            if error_on_empty:
                raise NoDataFound
            return None

        return Run(data["data"], http=self._http)
