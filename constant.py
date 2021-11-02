from enum import Enum

ROULETTE_START_RANGE = 1
ROULETTE_END_RANGE = 36


class GameStatus(Enum):
    OPEN = "open"
    CLOSE = "close"


class BetStatus(Enum):
    WON = "won"
    LOST = "lost"
    PENDING = "PENDING"
