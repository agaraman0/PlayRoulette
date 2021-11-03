from typing import Dict, Any, List

from exceptions import *
from models import *
from constant import ROULETTE_START_RANGE, ROULETTE_END_RANGE

from sqlalchemy import and_


def is_valid_number(number: int) -> bool:
    """
    Check if number is valid

    :param number: number range

    :return: check flag if number is in correct range
    """
    if ROULETTE_START_RANGE <= number <= ROULETTE_END_RANGE:
        return True
    return False


def is_casino_available(casino_id) -> bool:
    """
    Check if casino is available

    :param casino_id: id of casino

    :return: flag for casino
    """
    filters = [Casino.id == casino_id]
    with LocalSession(Session) as session:
        casino_obj = session.query(Casino).filter(and_(*filters)).first()
        if casino_obj.id:
            return True
    return False


def is_user_available(user_id: int) -> bool:
    """
    Check if user is available

    :param user_id: id of user

    :return: check flag if user is available
    """
    filters = [User.id == user_id]
    with LocalSession(Session) as session:
        casino_obj = session.query(User).filter(and_(*filters)).first()
        if casino_obj.id:
            return True
    return False


def is_game_correct(game_id: int, user_id: int) -> bool:
    """
    Game can be assigned or not

    :param game_id: id of open game
    :param user_id: id of user

    :return: if game can be assigned
    """
    with LocalSession(Session) as session:
        filters = [Game.id == game_id, User.id == user_id, Game.status == GameStatus.OPEN.value]
        game = session.query(Game)\
            .join(Dealer, Game.did == Dealer.id)\
            .join(Casino, Dealer.cid == Casino.id)\
            .join(User, Casino.id == User.cid)\
            .filter(and_(*filters)).first()
        if game.id:
            return True
    return False


def create_user(user_name: str) -> Dict[str, Any]:
    """
    Register User

    :param user_name: name of the user

    :return: user object
    """
    with LocalSession(Session) as session:
        user_obj = User(user_name)
        session.add(user_obj)
        session.flush()
    return user_obj.get_format()


def assign_casino(casino_id: int, user_id: int) -> Dict[str, Any]:
    """
    Assign Casino to user

    :param casino_id: id of casino
    :param user_id: id of user

    :return: assign casino to user

    :raises: CasinoNotFound
    """
    with LocalSession(Session) as session:
        if is_casino_available(casino_id):
            user_obj = session.query(User).filter(User.id == user_id).first()
            user_obj.cid = casino_id
            session.flush()
            return user_obj.get_format()
        else:
            raise CasinoNotFound


def list_all_games(user_id: int) -> List[Dict[str, Any]]:
    """
    List all games available for a user

    :param user_id: id of user

    :return: all available games for a user

    :raises: UserNotFound
    """
    with LocalSession(Session) as session:
        if is_user_available(user_id):
            filters = [User.id == user_id, Game.status == GameStatus.OPEN.value]
            games = session.query(Game).join(Dealer, Game.did == Dealer.id).join(Casino, Dealer.cid == Casino.id).join(
                User, Casino.id == User.cid).filter(and_(*filters)).all()
            games = [game.get_format() for game in games]
            return games
        raise UserNotFound


def add_amount_to_user_balance(user_id: int, amount: int) -> Dict[str, Any]:
    """
    Add amount to user balance

    :param user_id: id of user
    :param amount: amount needs to be added to user balance

    :return: user object with updated balance

    :raises: InsufficientAmount
    """
    with LocalSession(Session) as session:
        if is_user_available(user_id):
            user_obj = session.query(User).filter(User.id == user_id).first()
            user_obj.balance += amount
            session.flush()
            return user_obj.get_format()
        else:
            raise InsufficientAmount


def user_balance(user_id: int) -> Dict[str, Any]:
    """
    Get user balance

    :param user_id: id of user

    :return: user object with balance

    :raises: UserNotFound
    """
    with LocalSession(Session) as session:
        if is_user_available(user_id):
            user_obj = session.query(User).filter(User.id == user_id).first()
            return user_obj.get_format()
        else:
            raise UserNotFound


def make_bet(user_id: int, bet_amount: int, game_id: int, bet_number: int):
    """
    Make a bet on a bet number

    :param user_id:id of user
    :param bet_amount: amount on bet
    :param game_id: id of game
    :param bet_number: betting number

    :return: bet dict info object

    :raises: InsufficientAmount, GameNotAvailableForUser
    """
    with LocalSession(Session) as session:
        user_obj = session.query(User).filter(User.id == user_id).first()
        if user_obj.balance < bet_amount:
            raise InsufficientAmount
        elif is_game_correct(game_id, user_id):
            bet_object = Bet(bet_number, bet_amount, user_id, game_id)
            user_obj.balance = user_obj.balance - bet_amount
            session.add(bet_object)
            session.flush()
            return bet_object.get_format()
        else:
            raise GameNotAvailableForUser
