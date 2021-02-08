# speedrun.py

Simple async wrapper for speedrun.com's API

### Example

```python
import aiohttp
from speedrunpy import SpeedrunPy

src = SpeedrunPy(session=aiohttp.ClientSession())
games = await src.get_games("Super Mario Sunshine")
print(games[0].name)
print(games[0].id)

# output
Super Mario Sunshine
1kgr75w4
```
