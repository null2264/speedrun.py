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


__title__ = "speedrun.py"
__author__ = "null2264"
__license__ = "MIT"
__copyright__ = "Copyright 2021-present null2264"
__version__ = "21.8.2a"


from typing import Literal, NamedTuple

from . import utils
from .asset import Asset
from .client import Client
from .errors import *
from .game import Game
from .name import Name
from .page import Page
from .user import User
from .variable import Variable


class VersionInfo(NamedTuple):
    year: int
    month: int
    update: int
    releaselevel: Literal["alpha", "beta", "candidate", "final"]


version_info: VersionInfo = VersionInfo(
    year=21, month=8, update=2, releaselevel="alpha"
)
