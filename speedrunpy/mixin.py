from typing import List


class SRCObjectMixin:
    def __init__(self, payload: dict) -> None:
        self.links: List[dict] = payload["links"]
