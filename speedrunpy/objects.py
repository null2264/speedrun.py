class Page:

    __slots__ = ("data", "offset", "max", "size", "hasNextPage", "hasPrevPage")

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
        return "{} -> [size={}, max={}, hasNextPage={}]".format(
            self.offset, self.size, self.max, self.hasNextPage
        )

    def __getitem__(self, item):
        return self.data[item]


class Asset:

    __slots__ = ("url", "uri", "width", "height")

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

    __slots__ = (
        "rawData",
        "id",
        "name",
        "nameInt",
        "nameJapan",
        "nameTwitch",
        "abbreviation",
        "weblink",
        "releaseYear",
        "releaseDate",
        "assets",
        "moderators",
        "platforms",
        "levels",
        "categories",
    )

    def __init__(self, data: dict, embedded: bool = False, embeds: list = []):
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
        self.assets = {
            asset: Asset(gameData["assets"][asset])
            for asset in gameData["assets"]
            if gameData["assets"][asset]
        }

        # Stuff that overwritten by embeds
        self.moderators = gameData["moderators"]
        self.platforms = gameData["platforms"]

        if not embedded:
            # self.page = Pagination(pagination)
            if "levels" in embeds:
                self.levels = [
                    Level(lev, embedded=True) for lev in gameData["levels"]["data"]
                ]
            if "categories" in embeds:
                self.categories = [
                    Category(cat, embedded=True)
                    for cat in gameData["categories"]["data"]
                ]
            if "moderators" in embeds:
                self.moderators = [
                    Runner(mod, embedded=True) for mod in self.moderators["data"]
                ]
            if "platforms" in embeds:
                self.platforms = [
                    Platform(platform, embedded=True)
                    for platform in self.platforms["data"]
                ]

    def __str__(self):
        return self.name

    def __repr__(self):
        return "{} (ID: {} | {})".format(self.name, self.id, self.releaseYear)


class Times:

    __slots__ = ("rawData", "realtime", "realtimeNoLoads", "ingame", "primary")

    def __init__(self, data):
        """
        Object for `run.times`
        """
        self.rawData = data
        self.realtime = data["realtime_t"]
        self.realtimeNoLoads = data["realtime_noloads_t"]
        self.ingame = data["ingame_t"]
        self.primary = self.ingame or self.realtimeNoLoads or self.realtime


class Run:

    __slots__ = (
        "rawData",
        "id",
        "weblink",
        "game",
        "level",
        "category",
        "times",
        "videos",
        "comment",
        "datePlayed",
        "players",
        "place",
    )

    def __init__(self, data, embedded: bool = False, embeds: list = []):
        """
        Object for `/runs/`
        """
        self.rawData = data
        # runData = self.rawData if data.get("id", None) is not None else self.rawData["run"]
        runData = self.rawData.get("run", self.rawData)
        self.id = runData["id"]
        self.weblink = runData["weblink"]
        self.game = runData["game"]
        self.level = runData["level"]
        self.category = runData["category"]
        self.times = Times(runData["times"])

        try:
            self.videos = [vid["uri"] for vid in runData["videos"]["links"]]
        except TypeError:
            self.videos = []
        except Exception as exc:
            print(exc)
            self.videos = []

        self.comment = runData["comment"]
        self.datePlayed = runData["date"]

        # Stuff that overwritten by embeds
        self.players = runData["players"]

        if not embedded:
            for embed in embeds:
                spl = embed.split(".")
                if spl[0] == "category":
                    try:
                        _ = [spl[1]]
                    except IndexError:
                        _ = []
                    self.category = Category(
                        self.category["data"], embedded=True, embeds=_
                    )
                if spl[0] == "players":
                    self.players = [
                        Runner(runner, embedded=True) for runner in self.players["data"]
                    ]
        else:
            # Obtainable in `/leaderboards/`
            self.place = self.rawData.get("place", None)

    def __str__(self):
        return self.id


class Runner:
    __slots__ = ("rawData", "id", "type", "name", "nameInt", "nameJapan", "weblink")

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

        self.name = (
            runnerData["names"]["international"]
            if self.type == "user"
            else runnerData["name"]
        )
        self.nameInt = self.name
        self.nameJapan = (
            runnerData["names"]["japanese"] if self.type == "user" else None
        )

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

    __slots__ = ("rawData", "id", "name", "type", "values")

    def __init__(self, data, embedded=False):
        """
        Object for `variables`
        """
        self.rawData = data
        varData = self.rawData
        self.id = varData["id"]
        self.name = varData["name"]
        self.type = varData["scope"]["type"]
        values = varData["values"]["values"]
        self.values = [Value(value, values[value]) for value in values]


class Value:

    __slots__ = ("id", "label", "rules", "flags")

    def __init__(self, id, data):
        """
        Object for `values`
        """
        self.id = id
        self.label = data["label"]
        self.rules = data["rules"]
        self.flags = data["flags"]

    def __str__(self):
        return self.label


class Category:

    __slots__ = ("rawData", "id", "name", "weblink", "type", "rules", "variables")

    def __init__(self, data, embedded=False, embeds=[]):
        """
        Object for `category`
        """
        self.rawData = data
        # categoryData = self.rawData["data"][0] if not embedded else self.rawData
        categoryData = self.rawData.get("data", self.rawData)
        try:
            categoryData = categoryData[0]
        except KeyError:
            pass
        self.id = categoryData["id"]
        self.name = categoryData["name"]
        self.weblink = categoryData["weblink"]
        self.type = categoryData["type"]
        self.rules = categoryData["rules"]

        if not embedded:
            pass
        else:
            for embed in embeds:
                if embed == "variables":
                    self.variables = [
                        Variable(var) for var in categoryData["variables"]["data"]
                    ]

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
    def __init__(self, data, embedded=False, embeds: dict = []):
        """
        Object for `/leaderboards/`
        """
        self.rawData = data
        lbData = self.rawData["data"]
        self.runs = lbData["runs"]
        self.runs = [Run(run, embedded=True) for run in self.runs]
