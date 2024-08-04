import asyncio
from speedrunpy import Client


async def main():
    src = Client()
    games = await src.get_games(name="Super Mario Sunshine")
    game = games.data[0]
    print(game.id, game.name)
    await src.close()

asyncio.run(main())
