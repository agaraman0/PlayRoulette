import datetime

from helpers.constant import GameStatus, BetStatus
from db import *


class Casino(db.Model):
    __tablename__ = 'casino'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    balance = db.Column(db.Integer)

    def __init__(self, name):
        self.name = name
        self.balance = 0

    def __repr__(self):
        return '<id {}>'.format(self.id)

    def get_format(self):
        return {
            'casino_id': self.id,
            'casino_name': self.name,
            'balance': self.balance
        }


class Dealer(db.Model):
    __tablename__ = 'dealers'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    cid = db.Column(db.Integer, db.ForeignKey('casino.id'), nullable=False)
    casino = db.relationship('Casino', backref=db.backref('dealers', lazy=True))

    def __init__(self, name, cid):
        self.name = name
        self.cid = cid

    def __repr__(self):
        return '<id {}>'.format(self.id)

    def get_format(self):
        return {
            'id': self.id,
            'name': self.name,
            'casino_id': self.cid
        }


class Game(db.Model):
    __tablename__ = "games"

    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.String)
    number = db.Column(db.Integer)
    start_time = db.Column(db.DateTime)
    end_time = db.Column(db.DateTime)
    did = db.Column(db.Integer, db.ForeignKey('dealers.id'), nullable=False)
    dealers = db.relationship('Dealer', backref=db.backref('games', lazy=True))

    def __init__(self, dealer_id, status=GameStatus.OPEN.value):
        self.did = dealer_id
        self.status = status
        self.start_time = datetime.datetime.now()

    def __repr__(self):
        return '<id {}>'.format(self.id)

    def get_format(self):
        return {
            'game_id': self.id,
            'game_status': self.status,
            'start_time': self.start_time
        }


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String)
    balance = db.Column(db.Integer)
    cid = db.Column(db.Integer, db.ForeignKey('casino.id'))
    casino = db.relationship('Casino', backref=db.backref('users', lazy=True))

    def __init__(self, name):
        self.name = name
        self.balance = 0
        self.cid = None

    def __repr__(self):
        return '<id {}>'.format(self.id)

    def get_format(self):
        response = {
            'user_id': self.id,
            'user_name': self.name,
            'user_balance': self.balance
        }
        if self.cid is not None:
            response['casino_id'] = self.cid

        return response


class Bet(db.Model):
    __tablename__ = "bets"

    id = db.Column(db.Integer, primary_key=True)
    bet_number = db.Column(db.Integer)
    amount = db.Column(db.Integer)
    betting_time = db.Column(db.DateTime)
    status = db.Column(db.String)

    uid = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    users = db.relationship('User', backref=db.backref('bets', lazy=True))

    gid = db.Column(db.Integer, db.ForeignKey('games.id'), nullable=False)
    games = db.relationship('Game', backref=db.backref('bets', lazy=True))

    def __init__(self, bet_number, amount, user_id, game_id, status=BetStatus.PENDING.value):
        self.bet_number = bet_number
        self.amount = amount
        self.status = status
        self.uid = user_id
        self.gid = game_id
        self.betting_time = datetime.datetime.now()

    def __repr__(self):
        return '<id {}>'.format(self.id)

    def get_format(self):
        return {
            'bet_id': self.id,
            'bet_number': self.bet_number,
            'bet_amount': self.amount,
            'user_id': self.uid,
            'game_id': self.gid,
            'bet_status': self.status
        }
