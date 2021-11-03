from db import LocalSession, Session
from models import Casino, Dealer


def register_casino(name: str):
    """
    create casino object and insert in DB

    :param name: casino name

    :return: casino_id
    """
    with LocalSession(Session) as session:
        casino_obj = Casino(name)
        session.add(casino_obj)
        session.flush()
    return casino_obj.id


def add_dealer_to_casino(casino_id: int, dealer_name: str):
    """
    Create Dealer assigned to casino

    :param casino_id: casino id under which new dealer will be serving
    :param dealer_name: dealer name

    :return: dealer id which has been created
    """
    with LocalSession(Session) as session:
        dealer_obj = Dealer(dealer_name, casino_id)
        session.add(dealer_obj)
        session.flush()
    return dealer_obj.get_format()


def list_all_dealers(casino_id: int):
    """
    List all dealers associated with a casino

    :param casino_id: id of the casino

    :return: list all dealers associated to casino
    """
    with LocalSession(Session) as session:
        df_response = session.query(Dealer).filter(Dealer.cid == casino_id).all()
        df_response = [dealer.get_format() for dealer in df_response]
    return df_response


def add_balance_to_casino(casino_id: int, amount: int):
    """
    Recharge casino with amount

    :param amount: amount needs to be added to casino balance
    :param casino_id: id of the casino

    :return: casino balance
    """
    with LocalSession(Session) as session:
        df_response = session.query(Casino).filter(Casino.id == casino_id).first()
        df_response.balance += amount
        session.flush()
    return df_response.get_format()
