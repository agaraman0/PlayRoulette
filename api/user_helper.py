from models import *


from sqlalchemy import and_


def is_valid_number(number):
    if 1 <= number <= 36:
        return True
    return False


def is_casino_available(casino_id):
    filters = [Casino.id == casino_id]
    with LocalSession(Session) as session:
        casino_obj = session.query(Casino).filter(and_(*filters)).first()
        if casino_obj.id:
            return True
    return False


def is_user_available(user_id):
    filters = [User.id == user_id]
    with LocalSession(Session) as session:
        casino_obj = session.query(User).filter(and_(*filters)).first()
        if casino_obj.id:
            return True
    return False


def is_game_correct(game_id, user_id):
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
