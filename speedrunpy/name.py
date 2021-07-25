from typing import Optional


class Name:
    def __init__(self, payload: dict) -> None:
        self.international: Optional[str] = payload["international"]
        self.japanese: Optional[str] = payload["japanese"]
        self.twitch: Optional[str] = payload["twitch"]

    def __repr__(self) -> str:
        return "<Names international={0.international} japanese={0.japanese} twitch={0.twitch}>".format(
            self
        )

    def __str__(self) -> str:
        return self.international or self.twitch or self.japanese
