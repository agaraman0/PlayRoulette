from enum import Enum

ROULETTE_START_RANGE = 1
ROULETTE_END_RANGE = 36


class GameStatus(Enum):
    OPEN = "open"
    CLOSE = "close"
    ARCHIVE = "archive"


class BetStatus(Enum):
    WON = "won"
    LOST = "lost"
    PENDING = "PENDING"


FAILURE_RESPONSE = {"message": "Bad Request"}

SUCCESS_RESPONSE = {'message': 'success'}

PATH_NOT_FOUND = {"message": "path not found"}

SERVER_ERROR = {"message": "server error"}
