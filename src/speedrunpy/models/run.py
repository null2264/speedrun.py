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

from typing import TYPE_CHECKING, Any, Dict, List, Optional, Union

from . import game as _game
from . import user as _user
from .category import Category
from .guest import Guest
from ..http import HTTPClient
from .level import Level
from .mixin import SRCObjectWithAssetsMixin


if TYPE_CHECKING:
    from .game import Game
    from .user import PartialUser, User


class Run(SRCObjectWithAssetsMixin):
    __slots__ = ("id", "place", "game", "category", "level")

    def __init__(self, payload: Dict[str, Any], http: HTTPClient) -> None:
        super().__init__(payload=payload, http=http)

        self.place: int | None = payload.get("place", None)

        try:
            run = payload["run"]
        except:
            run = payload

        self.id: str = run["id"]

        # embeds
        game = payload["game"] if self.place is not None else run["game"]
        self.game: Game = _game.Game(game["data"], http=self._http)

        self.category: Category = Category(payload["category"]["data"], http=self._http)

        # Stupid SR.C, empty level is [], but non-empty level is {...}, why?
        _payload_level: Union[List[Any], Dict[str, Any]] = payload.get("level", [])
        level: Optional[Dict[str, Any]] = {} if isinstance(_payload_level, list) else _payload_level.get("data")
        self.level: Optional[Level] = None
        if level:
            self.level = Level(level, http=self._http)

        # FIXME: Player list is flatten in /leaderboards/ when `players` is embedded
        # REF: https://github.com/speedruncomorg/api/issues/81
        players: Optional[Dict[str, Any]] = payload.get("players")
        self.players: List[Union[User, PartialUser, Guest]] = list()
        if players:
            for i in players["data"]:
                if i["rel"] == "guest":
                    self.players.append(Guest(i))
                    continue

                self.players.append(
                    _user.User(i, http=self._http) if i.get("name") else _user.PartialUser(i, http=self._http)
                )

        region = payload.get("region")
        platform = payload.get("platform")
