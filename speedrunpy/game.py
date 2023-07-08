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

import datetime
from typing import TYPE_CHECKING, Any, Dict, List, Optional, Union

from .asset import Asset
from .category import Category
from .errors import NoDataFound
from .http import HTTPClient
from .level import Level
from .mixin import SRCObjectMixin
from .name import Name
from .page import Page
from .user import User
from .utils import zulu_to_utc
from .variable import Variable


if TYPE_CHECKING:
    from typing_extensions import (
        Self,  # type: ignore - for some reason I still get complain from my text editor
    )


class PartialGame(SRCObjectMixin):
    __slots__ = (
        "_http",
        "id",
        "name",
        "abbreviation",
        "weblink",
    )

    def __init__(self, payload: Dict[str, Any], http: HTTPClient) -> None:
        super().__init__(payload)

        self._http = http
        self.is_bulk = True

        # Dataset given in _bulk mode
        self.id: str = payload["id"]
        self.name: Name = Name(payload["names"])
        self.abbreviation: str = payload["abbreviation"]
        self.weblink: str = payload["weblink"]

    def __str__(self) -> Optional[str]:
        return self.name.international

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} id={self.id} name={self.name}>"

    def __eq__(self, other: Any) -> bool:
        return isinstance(other, PartialGame) and self.id == other.id

    def __ne__(self, other: Any) -> bool:
        return not self.__eq__(other)

    async def get_derived_games(
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
        _bulk: bool = False,
        offset: Optional[int] = None,
        max: Optional[int] = None,
        error_on_empty: bool = False,
    ) -> Page[Self]:
        """|coro|

        Get derived games
        """
        data = await self._http._derived_games(
            self.id,
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

        games: List[Self] = [cls(i, http=self._http) for i in data["data"]]

        if error_on_empty and not games:
            raise NoDataFound

        return Page(
            page_info=data["pagination"],
            data=games,
        )

    get_romhacks = get_derived_games

    async def get_records(self):
        pass


class Game(PartialGame):
    __slots__ = (
        "released",
        "_release_date",
        "ruleset",
        "romhack",
        "gametypes",
        "platforms",
        "regions",
        "genres",
        "engines",
        "developers",
        "publishers",
        "moderators",
        "_created",
        "assets",
        "levels",
        "categories",
        "variables",
    )

    def __init__(self, payload: Dict[str, Any], http: HTTPClient) -> None:
        super().__init__(payload, http)

        self.is_bulk = False

        self.released: int = payload["released"]
        self._release_date: str = payload["release-date"]
        self.ruleset: Dict[str, Union[bool, Any]] = payload["ruleset"]
        self.romhack: bool = payload["romhack"]
        self.gametypes: Dict[str, Any] = payload["gametypes"]
        self.platforms: Dict[str, Any] = payload["platforms"]
        self.regions: Dict[str, Any] = payload["regions"]
        self.genres: Dict[str, Any] = payload["genres"]
        self.engines: Dict[str, Any] = payload["engines"]
        self.developers: Dict[str, Any] = payload["developers"]
        self.publishers: Dict[str, Any] = payload["publishers"]

        moderators: Optional[List[Any]] = payload.get("moderators", dict()).get("data")
        self.moderators: List[User] = list()
        if moderators:
            # FIXME: Role is broken
            # - When moderators is embedded, mod role is replaced by site role
            #   REF: https://github.com/speedruncomorg/api/issues/17
            # - Even if that's not an issue, verifier role will always be seen as super-mod
            #   REF: https://github.com/speedruncomorg/api/issues/129
            #
            # Until both issue is fixed, I will hardcode role as moderator
            _m = []
            for i in moderators:
                mod = User(i, http=self._http)
                mod.role = "moderator"
                _m.append(mod)
            self.moderators = _m

        self._created: Optional[str] = payload.get("created")

        assets: Optional[Dict[str, Any]] = payload.get("assets")
        self.assets: Dict[str, Asset] = dict()
        if assets:
            self.assets = {
                k: Asset(v, http=self._http) for k, v in assets.items() if v["uri"]
            }

        levels: Optional[Dict[str, Any]] = payload.get("levels")
        self.levels: List[Level] = list()
        if levels:
            self.levels = [Level(i, http=self._http) for i in levels["data"]]

        categories: Optional[Dict[str, Any]] = payload.get("categories")
        self.categories: List[Category] = list()
        if categories:
            self.categories = [Category(i, http=self._http) for i in categories["data"]]

        variables: Optional[Dict[str, Any]] = payload.get("variables")
        self.variables: List[Variable] = list()
        if variables:
            self.variables = [Variable(i) for i in variables["data"]]

    @property
    def release_date(self) -> Optional[datetime.datetime]:
        if self._release_date:
            return datetime.datetime.fromisoformat(self._release_date).replace(
                tzinfo=datetime.timezone.utc
            )

    @property
    def created(self) -> Optional[datetime.datetime]:
        if self._created:
            created = zulu_to_utc(self._created)
            return datetime.datetime.fromisoformat(created)
