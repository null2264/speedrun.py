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
        self.assets: Dict[str, Asset] = {k: Asset(v, session) for k, v in payload["assets"].items()}# TODO: Create asset object

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
