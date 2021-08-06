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

from functools import wraps
from typing import TYPE_CHECKING, Any, Callable, Dict, TypeVar, Union

from .errors import AuthenticationRequired


C = TypeVar("C", bound="Client")
T = TypeVar("T")
if TYPE_CHECKING:
    from typing_extensions import Concatenate, ParamSpec

    from .client import Client

    B = ParamSpec("B")


try:
    import orjson

    JSON = orjson
except ImportError:
    import json

    JSON = json


def urlify(**kwargs) -> str:
    return "?" + "&".join(
        [
            f"{k}={str(v).replace(' ', '%20')}"
            for k, v in kwargs.items()
            if v is not None
        ]
    )


def zulu_to_utc(iso_datetime: str) -> str:
    return iso_datetime.rstrip("Z") + "+00:00"


def from_json(obj: Union[str, bytes]) -> Dict[str, Any]:
    return JSON.loads(obj)


def to_json(obj: Any) -> Union[str, bytes]:
    return JSON.dumps(obj)


def require_authentication(
    func: Callable[Concatenate[C, B], T]
) -> Callable[Concatenate[C, B], T]:
    @wraps(func)
    def wrapper(client: C, *args: B.args, **kwargs: B.kwargs) -> T:
        if not client._http._authenticated:
            raise AuthenticationRequired

        return func(client, *args, **kwargs)

    return wrapper
