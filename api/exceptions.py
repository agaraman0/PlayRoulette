class RouletteException(Exception):
    """

    """

    def __init__(self, code: str = "999", message: str = "Unknown error occurred"):
        """

        :param code:
        :param message:
        """
        self.code = code
        self.message = message

    def __str__(self):
        return repr("{} : {}".format(self.code, self.message))


class CasinoOutOfCash(RouletteException):
    """

    """

    def __init__(self, message: str = "Casino Out of balance"):
        """

        :param message:
        """
        super(CasinoOutOfCash, self).__init__(code="400", message=message)


class GameNotFoundToPlay(RouletteException):
    """

    """

    def __init__(self, message: str = "Game not found"):
        """

        :param message:
        """
        super(GameNotFoundToPlay, self).__init__(code="400", message=message)
