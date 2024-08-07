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

from typing import Any, Dict, List, Optional

from ..http import HTTPClient
from .mixin import SRCObjectMixin
from .variable import Variable


class Category(SRCObjectMixin):
    __slots__ = (
        "id",
        "name",
        "weblink",
        "type",
        "rules",
        "players",
        "misc",
        "_variables",
    )

    def __init__(self, payload: Dict[str, Any], http: HTTPClient) -> None:
        super().__init__(payload)

        self._http = http

        self.id: str = payload["id"]
        self.name: str = payload["name"]
        self.weblink: str = payload["weblink"]
        self.type: str = payload["type"]
        self.rules: str = payload["rules"]
        self.players: Dict[str, Any] = payload["players"]
        self.misc: bool = payload["miscellaneous"]

        self._variables: Optional[List[Dict[str, Any]]] = payload.get("variables", {}).get("data")
        self.__cached_variables: Optional[List[Variable]] = None

    async def fetch_variables(self) -> List[Variable]:
        data = await self._http._category_variables(self.id)
        self._variables = data["data"]
        self.__cached_variables = None
        return self.variables  # type: ignore

    async def getch_variables(self) -> List[Variable]:
        rt: Optional[List[Variable]] = self.variables
        if rt is None:
            rt = await self.fetch_variables()
        return rt

    @property
    def variables(self) -> Optional[List[Variable]]:
        # FIXME: If I embed "category.variables", sr.c sometime hangs and never send any response.
        # Hopefully v2 gonna fix this issue.
        if not self._variables:
            return None
        if not self.__cached_variables:
            self.__cached_variables = [Variable(i) for i in self._variables]
        return self.__cached_variables

    def __str__(self) -> str:
        return self.name

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} id={self.id} " f"name={self.name} type={self.type}>"
