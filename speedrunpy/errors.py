class RateLimited(Exception):
    def __init__(self):
        super().__init__("You're being rate limited")
