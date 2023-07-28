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

from typing import Any, Dict, Optional

from .mixin import SRCObjectMixin


class Variable(SRCObjectMixin):
    __slots__ = (
        "id",
        "name",
        "category",
        "type",
        "mandatory",
        "user_defined",
        "obsoletes",
        "values",
        "is_subcategory",
    )

    def __init__(self, payload: Dict[str, Any]) -> None:
        super().__init__(payload)

        self.id: str = payload["id"]
        self.name: str = payload["name"]
        self.category: Optional[str] = payload["category"]
        self.type: Optional[str] = payload.get("scope", {}).get("type")
        self.mandatory: bool = payload["mandatory"]
        self.user_defined: bool = payload["user-defined"]
        self.obsoletes: bool = payload["obsoletes"]
        self.values: Dict[str, Any] = payload["values"]
        self.is_subcategory: bool = payload["is-subcategory"]

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} id={self.id} name={self.name}>"
