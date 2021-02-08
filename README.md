# speedrun.py

Simple async wrapper for speedrun.com's API

### Example

```python
import aiohttp
from speedrunpy import SpeedrunPy

src = SpeedrunPy(session=aiohttp.ClientSession())
game = await src.get_game("Super Mario Sunshine")
print(game.name)
print(game.id)

# output
Super Mario Sunshine
1kgr75w4
```
