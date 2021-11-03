from api.exceptions import CasinoOutOfCash, GameNotFoundToPlay
from models import *
from sqlalchemy import and_
from random import randint
from constant import ROULETTE_START_RANGE, ROULETTE_END_RANGE


def create_game(dealer_id: int):
    """

    :param dealer_id:
    :return:
    """
    with LocalSession(Session) as session:
        if not is_dealer_assigned(dealer_id):
            game_obj = Game(dealer_id)
            session.add(game_obj)
            session.flush()


def is_dealer_assigned(dealer_id):
    filters = [Game.did == dealer_id, Game.status == GameStatus.OPEN.value]
    with LocalSession(Session) as session:
        game_objects = session.query(Game).filter(and_(*filters)).all()
        if len(game_objects) > 0:
            return True
    return False


def throw_number():
    return randint(ROULETTE_START_RANGE, ROULETTE_END_RANGE)


def update_all_bets(dealer_id, game_number):
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
        for bet in bets:
            if bet.bet_number == game.number:
                user = session.query(User).filter(User.id == bet.uid).first()
                if casino.balance < bet.amount:
                    raise CasinoOutOfCash
                casino.balance = casino.balance - bet.amount
                user.balance = user.balance + 2*bet.amount
                bet.status = BetStatus.WON.value
            else:
                casino.balance = casino.balance + bet.amount
                bet.status = BetStatus.LOST.value
        game.status = GameStatus.ARCHIVE.value
        session.flush()
