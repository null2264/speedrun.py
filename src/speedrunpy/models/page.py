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

from typing import Dict, Generic, List, TypeVar

from .mixin import SRCObjectMixin


T = TypeVar("T")


class Page(SRCObjectMixin, Generic[T]):
    __slots__ = ("offset", "max", "size", "data")

    def __init__(self, page_info: Dict[str, int], data: List[T]) -> None:
        super().__init__(page_info)

        self.offset: int = page_info["offset"]
        self.max: int = page_info["max"]
        self.size: int = page_info["size"]
        self.data: List[T] = data

    def __getitem__(self, index: int) -> T:
        return self.data[index]

    def __repr__(self) -> str:
        return (
            f"<{self.__class__.__name__} offset={self.offset} " f"max={self.max} size={self.size} data={self.data!r}>"
        )

    def __bool__(self) -> bool:
        return bool(self.data)
