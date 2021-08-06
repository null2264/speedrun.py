from typing import Any, Dict, List, TypedDict


class SpeedrunResponse(TypedDict):
    data: Dict[str, Any]


class SpeedrunPagedResponse(TypedDict):
    data: List[Dict[str, Any]]
    pagination: Dict[str, Any]
