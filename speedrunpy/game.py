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
from typing import Union, Dict, Optional, Iterable, Any, List


from .asset import Asset
from .http import HTTPClient
from .mixin import SRCObjectMixin
from .name import Name
from .user import User
from .utils import zulu_to_utc


class Game(SRCObjectMixin):
    __slots__ = (
        "id",
        "name",
        "abbreviation",
        "weblink",
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
    )

    def __init__(self, payload: dict, http: HTTPClient) -> None:
        super().__init__(payload)
        # TODO: Support _bulk mode
        self.id: str = payload["id"]
        self.name: Name = Name(payload["names"])
        self.abbreviation: str = payload["abbreviation"]
        self.weblink: str = payload["weblink"]
        self.released: int = payload["released"]
        self._release_date: str = payload["release-date"]
        self.ruleset: Dict[str, Union[bool, dict]] = payload["ruleset"]
        self.romhack: bool = payload["romhack"]
        self.gametypes: list = payload["gametypes"]
        self.platforms: list = payload["platforms"]
        self.regions: list = payload["regions"]
        self.genres: list = payload["genres"]
        self.engines: list = payload["engines"]
        self.developers: list = payload["developers"]
        self.publishers: list = payload["publishers"]
        self.moderators: List[User] = [User(i) for i in payload["moderators"]["data"]]
        self._created: str = payload["created"]
        self.assets: Dict[str, Asset] = {
            k: Asset(v, http) for k, v in payload["assets"].items()
        }

    def __str__(self) -> str:
        return self.name.international

    def __repr__(self) -> str:
        return f"<Games id={self.id} names={self.name}>"

    def __eq__(self, other: Any) -> bool:
        return isinstance(other, Game) and self.id == other.id

    def __ne__(self, other: Any) -> bool:
        return not self.__eq__(other)

    @property
    def release_date(self) -> datetime.datetime:
        return datetime.datetime.fromisoformat(self._release_date)

    @property
    def created(self) -> datetime.datetime:
        created = zulu_to_utc(self._created)
        return datetime.datetime.fromisoformat(created)
