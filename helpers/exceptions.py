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

        :param message: exception message
        """
        super(GameNotFoundToPlay, self).__init__(code="400", message=message)


class CasinoNotFound(RouletteException):
    """

    """
    def __init__(self, message: str = "Casino not Found"):
        """

        :param message: exception message
        """
        super(CasinoNotFound, self).__init__(code=400, message=message)


class UserNotFound(RouletteException):
    """

    """
    def __init__(self, message: str = "user Not found"):
        """

        :param message: exception message
        """
        super(UserNotFound, self).__init__(code=400, message=message)


class DealerAlreadyAssigned(RouletteException):
    """

    """
    def __init__(self, message: str = "Dealer is Already Assigned to a open game"):
        """

        :param message: exception message
        """
        super(DealerAlreadyAssigned, self).__init__(code=400, message=message)


class DealerHasNoActiveGame(RouletteException):
    """

    """
    def __init__(self, message: str = "Dealer has no active game"):
        """

        :param message: exception message
        """
        super(DealerHasNoActiveGame, self).__init__(code=400, message=message)


class InsufficientAmount(RouletteException):
    """

    """
    def __init__(self, message: str = "Amount is not sufficient"):
        """

        :param message: exception message
        """
        super(InsufficientAmount, self).__init__(code=400, message=message)


class GameNotAvailableForUser(RouletteException):
    """

    """
    def __init__(self, message: str = "Game not available for user under current casino"):
        """

        :param message:
        """
        super(GameNotAvailableForUser, self).__init__(code=400, message=message)


class NumberOutOfRange(RouletteException):
    """

    """
    def __init__(self, message: str = "Number is not available on board"):
        """

        :param message:
        """
        super(NumberOutOfRange, self).__init__(code=400, message=message)
