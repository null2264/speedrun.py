from typing import Any, Dict, List, TypedDict


class SpeedrunResponse(TypedDict):
    data: Dict[str, Any]


class SpeedrunPagedResponse(TypedDict):
    data: List[Dict[str, Any]]
    pagination: Dict[str, Any]


class GetUserSummaryResponse(TypedDict):
    user: Dict[str, Any]
    userProfile: Dict[str, Any]
    userStats: Dict[str, Any]
    userGameFollowerStats: List[Any]
    userGameModeratorStats: List[Any]
    userGameRunnerStats: List[Any]
    userSocialConnectionList: List[Any]
    games: List[Any]
    theme: Dict[str, Any]
    titleList: List[Any]
