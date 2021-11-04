from typing import Dict, Any

from helpers.exceptions import CasinoOutOfCash, GameNotFoundToPlay, DealerAlreadyAssigned, DealerHasNoActiveGame
from models import *
from sqlalchemy import and_, or_
from random import randint
from helpers.constant import ROULETTE_START_RANGE, ROULETTE_END_RANGE


def create_game(dealer_id: int) -> Dict[str, Any]:
    """
    Start new game assigned to dealer

    :param dealer_id: id of dealer

    :return: new game info dict

    :raises: DealerAlreadyAssigned
    """
    with LocalSession(Session) as session:
        if not is_dealer_assigned(dealer_id):
            game_obj = Game(dealer_id)
            session.add(game_obj)
            session.flush()
            return game_obj.get_format()
        else:
            raise DealerAlreadyAssigned


def stop_game_for_dealer(dealer_id: int) -> Dict[str, Any]:
    """
    Stop game assigned to dealer

    :param dealer_id: id of dealer

    :return: stop game dict info

    :raises: DealerHasNoActiveGame
    """
    with LocalSession(Session) as session:
        filters = [Game.did == dealer_id, Game.status == GameStatus.OPEN.value]
        game_obj = session.query(Game).filter(and_(*filters)).first()
        if game_obj.id:
            game_obj.status = GameStatus.CLOSE.value
            session.flush()
            return game_obj.get_format()
        else:
            raise DealerHasNoActiveGame


def is_dealer_assigned(dealer_id: int) -> bool:
    """
    Is dealer already assigned to some active game

    :param dealer_id: id of dealer

    :return: dealer assignment flag
    """
    game_or_filter = [Game.status == GameStatus.OPEN.value, Game.status == GameStatus.CLOSE.value]
    filters = [Game.did == dealer_id, or_(*game_or_filter)]
    with LocalSession(Session) as session:
        game_objects = session.query(Game).filter(and_(*filters)).all()
        if len(game_objects) > 0:
            return True
    return False


def throw_number() -> int:
    """
    throw number on table to get in between range

    :return: Winning Number for a game
    """
    return randint(ROULETTE_START_RANGE, ROULETTE_END_RANGE)


def update_all_bets(dealer_id: int, game_number: int) -> Dict[str, Any]:
    """
    Play game and settle up all bets

    :param dealer_id: id of dealer who thrown dice
    :param game_number: game winning number

    :return: Game Conclusion
    """
    with LocalSession(Session) as session:
        filters = [Game.did == dealer_id, Game.status == GameStatus.CLOSE.value]
        game = session.query(Game).filter(and_(*filters)).first()
        if not game:
            raise GameNotFoundToPlay
        bets_filters = [Game.id == game.id, Bet.status == BetStatus.PENDING.value]
        casino_filters = [Game.id == game.id, Game.status == GameStatus.CLOSE.value]
        game.number = game_number
        bets = session.query(Bet).join(Game, Bet.gid == Game.id).filter(and_(*bets_filters)).all()
        casino = session.query(Casino) \
            .join(Dealer, Casino.id == Dealer.cid) \
            .join(Game, Dealer.id == Game.did).filter(and_(*casino_filters)).first()
        winner = []
        for bet in bets:
            if bet.bet_number == game.number:
                user = session.query(User).filter(User.id == bet.uid).first()
                if casino.balance < bet.amount:
                    raise CasinoOutOfCash
                casino.balance = casino.balance - bet.amount
                user.balance = user.balance + 2*bet.amount
                bet.status = BetStatus.WON.value
                winner.append(bet.get_format())
            else:
                casino.balance = casino.balance + bet.amount
                bet.status = BetStatus.LOST.value
        game.status = GameStatus.ARCHIVE.value
        game.end_time = datetime.datetime.now()
        session.flush()
        return {
            "winning_bets": winner,
            "game": game.get_format(),
            "casino": casino.get_format()
        }
