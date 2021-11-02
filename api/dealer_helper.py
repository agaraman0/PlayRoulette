from models import *
from sqlalchemy import and_
from random import randint
from constant import ROULETTE_START_RANGE, ROULETTE_END_RANGE


def is_dealer_assigned(dealer_id):
    filters = [Game.did == dealer_id, Game.status == GameStatus.OPEN.value]
    with LocalSession(Session) as session:
        game_objects = session.query(Game).filter(and_(*filters)).all()
        if len(game_objects) > 0:
            return True
    return False


def throw_number():
    return randint(ROULETTE_START_RANGE, ROULETTE_END_RANGE)


def update_all_bets(game_id, game_number):
    bets_filters = [Game.id == game_id, Bet.status == BetStatus.PENDING.value]
    casino_filters = [Game.id == game_id, Game.status == GameStatus.CLOSE.value]
    with LocalSession(Session) as session:
        game = session.query(Game).filter(and_(*casino_filters)).first()
        game.number = game_number
        bets = session.query(Bet).join(Game, Bet.gid == Game.id).filter(and_(*bets_filters)).all()
        casino = session.query(Casino)\
            .join(Dealer, Casino.id == Dealer.id)\
            .join(Game, Dealer.id == Game.did).filter(and_(*casino_filters)).first()

        for bet in bets:
            if bet.bet_number == game.number:
                user = session.query(User).filter(User.id == bet.uid).first()
                if casino