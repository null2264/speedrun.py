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
from typing import Any, Dict, Optional

from .asset import Asset
from .http import HTTPClient
from .mixin import SRCObjectMixin
from .name import Name
from .utils import zulu_to_utc


class User(SRCObjectMixin):
    def __init__(self, payload: Dict[str, Any], http: HTTPClient) -> None:
        self._http = http

        self.id: str = payload["id"]
        self.name: Name = Name(payload["names"])
        self.pronouns: Optional[str] = payload["pronouns"]
        self.weblink: str = payload["weblink"]
        self.name_style: Dict[str, Any] = payload["name-style"]
        self.role: str = payload["role"]
        self._signup: str = payload["signup"]
        self.location: Optional[str] = payload["location"]
        self.twitch: Optional[str] = (payload["twitch"] or {}).get("uri", None)
        self.hitbox: Optional[str] = (payload["hitbox"] or {}).get("uri", None)
        self.youtube: Optional[str] = (payload["youtube"] or {}).get("uri", None)
        self.twitter: Optional[str] = (payload["twitter"] or {}).get("uri", None)
        self.speedrunslive: Optional[str] = (payload["speedrunslive"] or {}).get(
            "uri", None
        )

        assets: Optional[Dict[str, Any]] = payload.get("assets")
        self.assets: Optional[Dict[str, Asset]]
        if assets:
            self.assets = {
                k: Asset(v, http=self._http) for k, v in assets.items() if v["uri"]
            }

    def __str__(self) -> Optional[str]:
        return self.name.international

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} id={self.id} names={self.name}>"

    @property
    def signup(self) -> datetime.datetime:
        signup = zulu_to_utc(self._signup)
        return datetime.datetime.fromisoformat(signup)
