# speedrun.py

[![pdm-managed](https://img.shields.io/badge/pdm-managed-blueviolet)](https://pdm.fming.dev)

**WARNING**: This project is still WIP, breaking changes may happens a lot.

An asynchronous API wrapper for speedrun.com

## Coverage

### V1

| Name           | Status  | Comments                                 |
|----------------|---------|------------------------------------------|
| Authentication | ✓       |                                          |
| Categories     | ？      | Class only                               |
| Games          | ？      | `GET /games`, `GET /games/{id}`, `GET /games/{id}/derived-games` |
| Guests         | ？      | Class only                               |
| Leaderboards   | ？      | Class only                               |
| Levels         | ？      | Class only                               |
| Notifications  | ？      |                                          |
| Platforms      | ？      |                                          |
| Profile        | ✓       |                                          |
| Publishers     | ？      |                                          |
| Regions        | ？      |                                          |
| Runs           | ？      | `GET /runs`, `GET /runs/{id}`            |
| Series         | ？      |                                          |
| Users          | ？      | TODO: check the coverage                 |
| Variables      | ？      | Class only                               |

### V2

As of writing this (2023-08-26), V2 is undocumented, may break at anytime.

| Function                | Status | Comments                         |
|-------------------------|--------|----------------------------------|
| GetSearch               | ？     |                                  |
| GetCommentList          | ？     |                                  |
| PutAuthSignup           | ？     |                                  |
| PutGameBoostGrant       | ？     |                                  |
| GetGameData             | ？     |                                  |
| GetConversations        | ？     |                                  |
| GetNotifications        | ？     |                                  |
| GetModerationGames      | ？     |                                  |
| GetSession              | ？     |                                  |
| GetGameSettings         | ？     |                                  |
| PutGameSettings         | ？     |                                  |
| GetThemeSettings        | ？     |                                  |
| GetAuditLogList         | ？     |                                  |
| GetModerationRuns       | ？     |                                  |
| PutSessionPing          | ？     |                                  |
| GetGameLeaderboard2     | ？     |                                  |
| GetGameRecordHistory    | ？     |                                  |
| GetConversationMessages | ？     |                                  |
| GetForumList            | ？     |                                  |
| GetForumReadStatus      | ？     |                                  |
| GetThreadReadStatus     | ？     |                                  |
| GetCommentable          | ？     |                                  |
| PutThreadRead           | ？     |                                  |
| GetThread               | ？     |                                  |
| GetUserSummary          | ？     | Incomplete                       |
| GetUserBlocks           | ？     |                                  |

#### Useful Links

- [V2 Unofficial Docs](https://github.com/ManicJamie/speedruncom-apiv2-docs) by [@ManicJamie](https://github.com/ManicJamie)
- [V2 Deno API wrapper and Documentation](https://git.sr.ht/~aninternettroll/speedruncomapiv2) by [@aninternettroll@git.sr.ht](https://git.sr.ht/~aninternettroll)
