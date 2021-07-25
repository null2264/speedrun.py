from typing import Any, List


class Page:
    __slots__ = ("offset", "max", "size", "links", "data")

    def __init__(self, page_info: dict, data: List[dict], cls: Any, session = None) -> None:
        self.offset: int = page_info["offset"]
        self.max: int = page_info["max"]
        self.size: int = page_info["size"]
        self.links: list = page_info["links"]
        self.data: List[Any] = [cls(i, session=session) for i in data]
