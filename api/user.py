from flask import jsonify, Blueprint, make_response, request
from sqlalchemy import and_

from api.user_helper import is_casino_available, is_user_available, is_game_correct
from constant import SERVER_ERROR
from models import *

user = Blueprint("user", __name__, url_prefix="/user/v1")


@user.errorhandler(Exception)
def handle_500_error(_error):
    """Return a http 500 error to client"""
    print(_error)
    return make_response(jsonify(SERVER_ERROR), 500)


@user.route('/register', methods=["POST"])
def register_user():
    json_args = request.json
    user_name = json_args.get('name')
    user_obj = User(user_name)
    with LocalSession(Session) as session:
        session.add(user_obj)
        session.flush()
    return make_response(jsonify({
        'message': "success",
        'data': {
            'id': user_obj.id
        }
    }), 200)


@user.route('/<user_id>/enter_casino', methods=["PUT"])
def enter_casino(user_id):
    json_args = request.json
    casino_id = json_args.get('casino_id')
    with LocalSession(Session) as session:
        if is_casino_available(casino_id):
            user_obj = session.query(User).filter(User.id == user_id).first()
            user_obj.cid = casino_id
            session.flush()
        else:
            return make_response(jsonify({
                'message': "failed",
                'data': {
                    'details': "casino not found with id {}".format(casino_id)
                }
            }), 400)
    return make_response(jsonify({
        'message': "success",
        'data': {
            'id': user_obj.id,
            'details': "{} has been entered in casino {}".format(user_obj.id, casino_id)
        }
    }), 200)


@user.route('/<user_id>/recharge', methods=["PUT"])
def recharge_user_balance(user_id):
    json_args = request.json
    amount = json_args.get('amount')
    with LocalSession(Session) as session:
        if is_user_available(user_id):
            user_obj = session.query(User).filter(User.id == user_id).first()
            user_obj.balance = amount
            session.flush()
        else:
            return make_response(jsonify({
                'message': "failed",
                'data': {
                    'details': "User Not Found"
                }
            }), 400)
    return make_response(jsonify({
        'message': "success",
        'data': {
            'id': user_obj.id,
            'details': "{} has recharged with amount {}".format(user_obj.id, amount)
        }
    }), 200)


@user.route('/<user_id>/cashout', methods=['GET'])
def get_user_balance(user_id):
    with LocalSession(Session) as session:
        if is_user_available(user_id):
            user_obj = session.query(User).filter(User.id == user_id).first()
        else:
            return make_response(jsonify({
                'message': "failed",
                'data': {
                    'details': "User Not Found"
                }
            }), 400)
    return make_response(jsonify({
        'message': "success",
        'data': {
            'id': user_obj.id,
            'details': "{} can cashout with amount {}".format(user_obj.name, user_obj.balance)
        }
    }), 200)


@user.route('/<user_id>/games_available', methods=['GET'])
def get_available_games(user_id):
    with LocalSession(Session) as session:
        if is_user_available(user_id):
            filters = [User.id == user_id, Game.status == GameStatus.OPEN.value]
            games = session.query(Game).join(Dealer, Game.did == Dealer.id).join(Casino, Dealer.cid == Casino.id).join(
                User, Casino.id == User.cid).filter(and_(*filters)).all()
            games = [game.get_format() for game in games]
    return make_response(jsonify({
        'message': "success",
        'data':  games
    }), 200)


@user.route('/<user_id>/bet', methods=['POST'])
def bet_on_game(user_id):
    json_args = request.json
    bet_number = json_args.get('lucky_number')
    bet_amount = json_args.get('amount')
    game_id = json_args.get('game_id')
    with LocalSession(Session) as session:
        user_obj = session.query(User).filter(User.id == user_id).first()
        if user_obj.balance < bet_amount:
            return make_response(jsonify({
                'message': "failed",
                'data': {
                    'details': "User does not have efficient amount"
                }
            }), 400)
        elif is_game_correct(game_id, user_id):
            bet_object = Bet(bet_number, bet_amount, user_id, game_id)
            user_obj.balance = user_obj.balance - bet_amount
            session.add(bet_object)
            session.flush()
        else:
            return make_response(jsonify({
                'message': "failed",
                'data': {
                    'details': "Game Not found for user with this game id {}".format(game_id)
                }
            }), 400)
    return make_response(jsonify({
        'message': "success",
        'data':  {
            'details': "Bet successfully Done on your lucky number {}".format(bet_number),
            'serial_id': bet_object.id
        }
    }), 200)
