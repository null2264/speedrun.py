def urlify(**kwargs):
    return "?" + "&".join(
        [
            f"{k}={str(v).replace(' ', '%20')}"
            for k, v in kwargs.items()
            if v is not None
        ]
    )
