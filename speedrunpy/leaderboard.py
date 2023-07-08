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

from typing import TYPE_CHECKING, Any, Dict, Union

from .category import Category
from .http import HTTPClient
from .mixin import SRCObjectMixin
from .run import Run


if TYPE_CHECKING:
    from .game import Game


class Leaderboard(SRCObjectMixin):
    def __init__(
        self, payload: Dict[str, Any], http: HTTPClient,
    ) -> None:
        self._http: HTTPClient = http

        game: Union[str, Dict[str, Any]] = payload["game"]
        if isinstance(game, dict) and http:
            self.game: Union[str, Game] = Game(game["data"], http=http)
        elif isinstance(game, str):
            self.game = game
        else:
            self.game = game["data"]["id"]

        self.category = Category(payload["categories"]["data"], http=self._http)
        self.runs: list[Run] = [Run(i, http=self._http) for i in payload["runs"]]
