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
from typing import Any, Dict, List, Optional

from .errors import NoDataFound
from .http import HTTPClient
from .mixin import SRCObjectWithAssetsMixin
from .name import Name
from .run import Run
from .utils import zulu_to_utc


class PartialUser:
    def __init__(self, payload: Dict[str, Any], http: HTTPClient) -> None:
        self._http: HTTPClient = http
        self.id: str = payload["id"]
        self.is_extended = False

    def __str__(self) -> str:
        return self.id

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} id={self.id}>"

    async def extend(self) -> User:
        if self.is_extended:
            raise RuntimeError("User already extended!")

        data = await self._http._user_by_id(self.id)

        return User(data["data"], http=self._http)


class User(PartialUser, SRCObjectWithAssetsMixin):
    def __init__(self, payload: Dict[str, Any], http: HTTPClient) -> None:
        super().__init__(payload, http)
        self.is_extended = True

        self.name: Name = Name(payload["names"])
        self.pronouns: str = payload["pronouns"]
        self.weblink: str = payload["weblink"]
        self.name_style: Dict[str, Any] = payload["name-style"]
        self.role: str = payload["role"]
        self._signup: str = payload["signup"]
        self.location: Optional[str] = payload["location"]
        self.twitch: Optional[str] = (payload["twitch"] or {}).get("uri", None)
        self.hitbox: Optional[str] = (payload["hitbox"] or {}).get("uri", None)
        self.youtube: Optional[str] = (payload["youtube"] or {}).get("uri", None)
        self.twitter: Optional[str] = (payload["twitter"] or {}).get("uri", None)
        self.speedrunslive: Optional[str] = (payload["speedrunslive"] or {}).get("uri", None)

    def __str__(self) -> Optional[str]:
        return self.name.international

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} id={self.id} names={self.name}>"

    @property
    def signup(self) -> datetime.datetime:
        signup = zulu_to_utc(self._signup)
        return datetime.datetime.fromisoformat(signup)

    async def get_personal_bests(self, error_on_empty: bool = False) -> List[Run]:
        data: Dict[str, Any] = await self._http._user_personal_bests(id=self.id)  # type: ignore
        runs: List[Run] = [Run(i, self._http) for i in data["data"]]

        if error_on_empty and not runs:
            raise NoDataFound

        return runs
