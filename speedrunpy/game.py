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
from typing import Any, Dict, List, Optional, Union

from .asset import Asset
from .category import Category
from .http import HTTPClient
from .level import Level
from .mixin import SRCObjectMixin
from .name import Name
from .user import User
from .utils import zulu_to_utc
from .variable import Variable


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
        "levels",
        "categories",
        "variables",
    )

    def __init__(self, payload: Dict[str, Any], http: HTTPClient) -> None:
        super().__init__(payload)

        # Dataset given in _bulk mode
        self.id: str = payload["id"]
        self.name: Name = Name(payload["names"])
        self.abbreviation: str = payload["abbreviation"]
        self.weblink: str = payload["weblink"]

        # Optionals (will always returns None when _bulk mode active)
        self.released: Optional[int] = payload.get("released")
        self._release_date: Optional[str] = payload.get("release-date")
        self.ruleset: Optional[Dict[str, Union[bool, Dict]]] = payload.get("ruleset")
        self.romhack: Optional[bool] = payload.get("romhack")
        self.gametypes: Optional[list] = payload.get("gametypes")
        self.platforms: Optional[list] = payload.get("platforms")
        self.regions: Optional[list] = payload.get("regions")
        self.genres: Optional[list] = payload.get("genres")
        self.engines: Optional[list] = payload.get("engines")
        self.developers: Optional[list] = payload.get("developers")
        self.publishers: Optional[list] = payload.get("publishers")

        moderators: Optional[Dict] = payload.get("moderators", dict()).get("data")
        self.moderators: Optional[List[User]] = None
        if moderators:
            # NOTE: This will NOT include moderator's role,
            # Because mod role is broken (verifier referred as super-mod in the api)
            self.moderators = [User(i) for i in moderators]

        self._created: Optional[str] = payload.get("created")

        assets: Optional[Dict] = payload.get("assets")
        self.assets: Optional[Dict[str, Asset]] = None
        if assets:
            self.assets = {k: Asset(v, http=http) for k, v in payload["assets"].items()}

        levels: Optional[Dict] = payload.get("levels")
        self.levels: Optional[List[Level]] = None
        if levels:
            self.levels = [Level(i) for i in levels["data"]]

        categories: Optional[Dict] = payload.get("categories")
        self.categories: Optional[List[Category]] = None
        if categories:
            self.categories = [Category(i) for i in categories["data"]]

        variables: Optional[Dict] = payload.get("variables")
        self.variables: Optional[List[Variable]] = None
        if variables:
            self.variables = [Variable(i) for i in variables["data"]]

    def __str__(self) -> Optional[str]:
        return self.name.international

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} id={self.id} name={self.name}>"

    def __eq__(self, other: Any) -> bool:
        return isinstance(other, Game) and self.id == other.id

    def __ne__(self, other: Any) -> bool:
        return not self.__eq__(other)

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
