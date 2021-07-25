class SRCObjectMixin:
    def __init__(self, payload: dict) -> None:
        self.links: dict = payload["links"]
