import aiohttp
import json
import urllib.parse


from contextlib import contextmanager


from .errors import DataNotFound
from .objects import (
    Category,
    Game,
    Leaderboard,
    Page,
    Run,
)


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
            data = json.loads(await res.text())
            try:
                if data["status"] == 404:
                    raise DataNotFound
                if data["status"] == 420:
                    # Reached request limit
                    return None
            except KeyError:
                return data

    def get_embeds(self, queries, choices):
        validQuery = []
        for query in queries:
            spl = query.split(".")
            if spl[0] in choices:
                validQuery += [query]
        return validQuery

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

        name = kwargs.pop("name", None)
        if not name:
            name = kwargs.pop("game", None)
        embeds = kwargs.pop("embeds", [])
        page = kwargs.pop("page", 0)
        perPage = kwargs.pop("perPage", 100)

        params = {
            "game": name or "",
            "embed": ",".join(self.get_embeds(embeds, availableEmbeds)),
            "max": perPage,
            "offset": perPage*page,
            **kwargs
        }
        query = urllib.parse.urlencode(params)
        runs = await self.get("/runs", "?{}".format(query))
        return Page([Run(run, embeds=embeds) for run in runs["data"]], runs["pagination"])
    
    async def get_categories(self, **kwargs):
        game = kwargs.pop("game", kwargs.pop("name", None))
        category = kwargs.pop("category", None)
        
        availableEmbeds = ("variables")
        if category:
            availableEmbeds+= ("games",)
        
        _type = "/games/{}/categories".format(game) if not category else "/categories/{}".format(category)

        embeds = kwargs.pop("embeds", [])
        page = kwargs.pop("page", 0)
        perPage = kwargs.pop("perPage", 100)

        params = {
            "embed": ",".join(self.get_embeds(embeds, availableEmbeds)),
            "max": perPage,
            "offset": perPage*page,
            **kwargs
        }
        query = urllib.parse.urlencode(params)
        cats = await self.get(_type, "?{}".format(query))
        return [Category(cat, embeds=embeds) for cat in cats["data"]] if isinstance(cats["data"], list) else Category(cats, embeds=embeds)

    async def get_leaderboards(self, game: str, **kwargs):
        availableEmbeds = (
            "game",
            "category",
            "level",
            "players",
            "regions",
            "platforms",
            "variables",
        )
        category = kwargs.pop("category", None)
        if not category:
            categories = await self.get_categories(name=game)
            category = categories[0].id
        level = kwargs.pop("level", None)
        embeds = kwargs.pop("embeds", [])
        page = kwargs.pop("page", 0)
        perPage = kwargs.pop("perPage", 100)

        _type = "/leaderboards/{}/category/{}".format(game, category) if not level else "/leaderboards/{}/level/{}/{}".format(game, level, category)

        params = {
            "embed": ",".join(self.get_embeds(embeds, availableEmbeds)),
            "max": perPage,
            "offset": perPage*page,
            **kwargs
        }
        query = urllib.parse.urlencode(params)
        lb = await self.get(_type, "?{}".format(query))
        return Leaderboard(lb, embeds=embeds)
