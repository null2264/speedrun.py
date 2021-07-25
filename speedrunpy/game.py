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


import datetime
from typing import Union, Dict
from aiohttp import ClientSession


from .asset import Asset
from .mixin import SRCObjectMixin
from .name import Name


class Game(SRCObjectMixin):
    def __init__(self, payload: dict, session: ClientSession) -> None:
        super().__init__(payload)
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
        self.moderators: list = payload["moderators"]
        self._created: str = payload["created"]
        self.assets: Dict[str, Asset] = {
            k: Asset(v, session) for k, v in payload["assets"].items()
        }  # TODO: Create asset object

    def __repr__(self) -> str:
        return "<Games id={0.id} names={0.names}>".format(self)

    def __str__(self) -> str:
        return self.name.international

    @property
    def release_date(self) -> datetime.datetime:
        return datetime.datetime.fromisoformat(self._release_date)

    @property
    def created(self) -> datetime.datetime:
        created = self._created.rstrip("Z") + "+00:00"
        return datetime.datetime.fromisoformat(created)
