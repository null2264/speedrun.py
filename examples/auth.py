import asyncio
from src.speedrunpy import Client


async def main():
    src = Client(token="your-api-token-goes-here")
    profile = await src.get_profile(error_on_empty=False)
    if profile:
        print(profile.id, profile.name)
    await src.close()

asyncio.run(main())
