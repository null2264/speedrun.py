from aiohttp import ClientSession
from typing import Optional


__all__ = (
    "Asset"
)


async def get_from_url(url, session: ClientSession) -> Optional[bytes]:
    async with session.get(url) as res:
        return await res.read()


class Asset:
    __slots__ = ("url", "_session")

    def __init__(self, payload: dict, session: ClientSession) -> None:
        self.url = payload["uri"]
        self._session = session

    def __repr__(self) -> str:
        return "<Asset url={}>".format(self.url)

    async def read(self):
        return await get_from_url(self.url, self._session)
