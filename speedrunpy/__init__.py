"""
MIT License

Copyright (c) 2021 null2264

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

import asyncio
import aiohttp
import json
import urllib.parse


from fuzzywuzzy import process


class Page:
    def __init__(self, data: list, pageData):
        """
        Object for `data.pagination`
        """
        self.data = data
        self.offset = pageData["offset"]
        self.max = pageData["max"]
        self.size = pageData["size"]
        self.hasNextPage = False
        self.hasPrevPage = False
        for i in pageData["links"]:
            self.hasNextPage = i.get("rel", None) == "next"
            self.hasPrevPage = i.get("rel", None) == "prev"

    def __str__(self):
        return "{} -> [size={}, max={}, hasNextPage={}]".format(self.offset, self.size, self.max, self.hasNextPage)

    def __getitem__(self, item):
         return self.data[item]


class Asset:
    def __init__(self, data):
        """
        Object for `asset`
        """
        self.url = data["uri"]
        self.uri = self.url
        self.width = data["width"]
        self.height = data["height"]

    def __str__(self):
        return self.url

    def __repr__(self):
        return "<{} ({}x{})>".format(self.url, self.width, self.height)


class Game:
    def __init__(self, data: dict, embedded: bool=False, embeds: list=[]):
        """
        Object for `/games/`
        """
        self.rawData = data
        gameData = self.rawData

        self.id = gameData["id"]
        self.name = gameData["names"]["international"]
        self.nameInt = self.name
        self.nameJapan = gameData["names"]["japanese"]
        self.nameTwitch = gameData["names"]["twitch"]
        self.abbreviation = gameData["abbreviation"]
        self.weblink = gameData["weblink"]
        self.releaseYear = gameData["released"]
        self.releaseDate = gameData["release-date"]
        self.assets = {asset: Asset(gameData["assets"][asset]) for asset in gameData["assets"] if gameData["assets"][asset]}

        # Stuff that overwritten by embeds
        self.moderators = gameData["moderators"]
        self.platforms = gameData["platforms"]

        if not embedded:
            # self.page = Pagination(pagination)
            if "levels" in embeds:
                self.levels = [Level(lev, embedded=True) for lev in gameData["levels"]["data"]]
            if "categories" in embeds:
                self.categories = [Category(cat, embedded=True) for cat in gameData["categories"]["data"]]
            if "moderators" in embeds:
                self.moderators = [Runner(mod, embedded=True) for mod in self.moderators["data"]]
            if "platforms" in embeds:
                self.platforms = [Platform(platform, embedded=True) for platform in self.platforms["data"]] 

    def __str__(self):
        return self.name

    def __repr__(self):
        return "{} (ID: {} | {})".format(self.name, self.id, self.releaseYear)


class Run:
    def __init__(self, data, embedded: bool=False, embeds: list=[]):
        """
        Object for `/runs/`
        """
        self.rawData = data
        runData = self.rawData if data.get("id", None) is not None else self.rawData["run"]
        self.id = runData["id"]
        self.weblink = runData["weblink"]
        self.game = runData["game"]
        self.level = runData["level"]
        self.category = runData["category"]

        try:
            self.videos = [vid["uri"] for vid in runData["videos"]["links"]]
        except TypeError:
            self.videos = []
        except Exception as exc:
            print(exc)
            self.video = []

        self.comment = runData["comment"]
        self.datePlayed = runData["date"]

        # Stuff that overwritten by embeds
        self.players = runData["players"]

        if not embedded:
            # self.page = Pagination(pagination)
            if process.extractOne("category", embeds)[1] >= 90:
                self.category = Category(self.category["data"], embedded=True)
            if "players" in embeds:
                self.players = [Runner(runner, embedded=True) for runner in self.players["data"]]
        else:
            # Obtainable in `/leaderboards/`
            self.place = self.rawData.get("place", None)

    def __str__(self):
        return self.id


class Runner:
    def __init__(self, data, embedded=False):
        """
        Object for Runner (`moderator`, `player`, `user`)
        """
        self.rawData = data
        runnerData = self.rawData["data"][0] if not embedded else self.rawData
        
        try:
            self.id = runnerData["id"]
            self.type = "user"
        except KeyError:
            self.id = None
            self.type = "guest"
        
        self.name = runnerData["names"]["international"] if self.type == "user" else runnerData["name"]
        self.nameInt = self.name
        self.nameJapan = runnerData["names"]["japanese"] if self.type == "user" else None

        self.weblink = runnerData["weblink"] if self.type == "user" else None

    def __str__(self):
        return self.name


class Platform:
    def __init__(self, data, embedded=False):
        """
        Object for `platform`
        """
        self.rawData = data
        platformData = self.rawData["data"] if not embedded else self.rawData
        self.id = platformData["id"]
        self.name = platformData["name"]
        self.releaseYear = platformData["released"]

    def __str__(self):
        return self.name


class Variable:
    def __init__(self, data, embedded=False):
        """
        Object for `variables`
        """
        self.rawData = data
        varData = self.rawData
        self.id = varData["id"]


class Category:
    def __init__(self, data, embedded=False):
        """
        Object for `category`
        """
        self.rawData = data
        categoryData = self.rawData["data"][0] if not embedded else self.rawData
        self.id = categoryData["id"]
        self.name = categoryData["name"]
        self.weblink = categoryData["weblink"]
        self.type = categoryData["type"]
        self.rules = categoryData["rules"]
        self.variables = categoryData.get("variables", None)

        if not embedded:
            pass
        else:
            if self.variables:
                self.variables = [Variable(var) for var in self.variables["data"]]
            
    
    def __str__(self):
        return self.name


class Level:
    def __init__(self, data, embedded=False):
        """
        Object for `level` (individual levels)
        """
        self.rawData = data
        levelData = self.rawData["data"][0] if not embedded else self.rawData
        self.id = levelData["id"]
        self.name = levelData["name"]
        self.weblink = levelData["weblink"]
    
    def __str__(self):
        return self.name


class Leaderboard:
    def __init__(self, data, embedded=False, embeds: dict=[]):
        """
        Object for `/leaderboards/`
        """
        self.rawData = data
        lbData = self.rawData["data"]
        self.runs = lbData["runs"]
        self.runs = [Run(run, embedded=True) for run in self.runs]


class SpeedrunPy:
    def __init__(self, session = aiohttp.ClientSession()):
        """
        Wrapper for speedrun.com's API
        """
        self.session = session
        self.baseUrl = "https://www.speedrun.com/api/v1"
    
    async def get(self, _type: str, query: str):
        """
        Get data from speedrun.com api

        Parameters
        ----------
        _type
            Type of request (example: `/games/{query}`)
        query
            Query for a request (example: `/games/mcbe` or `/games?name=Minecraft: Bedrock Edition`)
        """
        async with self.session.get(self.baseUrl + _type + query) as res:
            return json.loads(await res.text())

    def get_embeds(self, query, choices):
        return [q for q in query if process.extractOne(q, choices)[1] > 85]

    async def get_games(self, name: str="", **kwargs):
        """
        Get game data from speedrun.com api

        Parameters
        ----------
        name
            Name/Abbreviation of the game
        page
            Page count
        perPage
            Game per page
        embeds
            SRC's Embeds
        """
        availableEmbeds = (
            "levels",
            "categories",
            "moderators",
            "gametypes",
            "platforms",
            "regions",
            "genres",
            "engines",
            "developers",
            "publishers",
            "variables",
        )

        embeds = kwargs.pop("embeds", [])
        page = kwargs.pop("page", 0)
        perPage = kwargs.pop("perPage", 100)

        params = {
            "name": name,
            "embed": ",".join(self.get_embeds(embeds, availableEmbeds)),
            "max": perPage,
            "offset": perPage*page,
            **kwargs,
        }
        query = urllib.parse.urlencode(params)
        games = await self.get("/games", "?{}".format(query))
        return Page([Game(game, embeds=embeds) for game in games["data"]], games["pagination"])

    async def get_runs(self, **kwargs):
        """
        Get runs data from speedrun.com api

        Parameters
        ----------
        name
            Name/Abbreviation of the game
        page
            Page count
        perPage
            Game per page
        embeds
            SRC's Embeds
        """
        availableEmbeds = (
            "game",
            "category",
            "level",
            "players",
            "region",
            "platform",
        )

        name = kwargs.pop("name", "")
        embeds = kwargs.pop("embeds", [])
        page = kwargs.pop("page", 0)
        perPage = kwargs.pop("perPage", 100)

        params = {
            "game": name, 
            "embed": ",".join(self.get_embeds(embeds, availableEmbeds)),
            "max": perPage,
            "offset": perPage*page,
            **kwargs
        }
        query = urllib.parse.urlencode(params)
        runs = await self.get("/runs", "?{}".format(query))
        return Page([Run(run, embeds=embeds) for run in runs["data"]], runs["pagination"])
    
    async def get_leaderboards(self, game: str, category: str, **kwargs):
        availableEmbeds = (
            "game",
            "category",
            "level",
            "players",
            "regions",
            "platforms",
            "variables",
        )
        level = kwargs.pop("level", None)
        embeds = kwargs.pop("embeds", [])
        page = kwargs.pop("page", 0)
        perPage = kwargs.pop("perPage", 100)

        _type = "/leaderboards/{}/category/{}".format(game, category) if not level else "/leaderboards/{}/level/{/{}".format(game, level, category)

        params = {
            "embed": ",".join(self.get_embeds(embeds, availableEmbeds)),
            "max": perPage,
            "offset": perPage*page,
            **kwargs
        }
        query = urllib.parse.urlencode(params)
        lb = await self.get(_type, "?{}".format(query))
        return Leaderboard(lb, embeds=embeds)


# Testing stuff
if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    src = SpeedrunPy()
    # res = await src.get_game("Super Mario Sunshine", embeds=["platforms"])
    # games = loop.run_until_complete(src.get_games("Minecraft: Bedrock Edition", embeds=["categories"]))
    # print(games.hasNextPage)
    # print(games[0].id)
    runs = loop.run_until_complete(src.get_runs(embeds=["category.variables"]))
    print(runs[0].category.variables[0].name)
    # lb = loop.run_until_complete(src.get_leaderboards(games[0].id, category=games[0].categories[0].id))
    # print(lb.runs[0].place)
