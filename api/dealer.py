from flask import jsonify, Blueprint, make_response
from sqlalchemy import and_

from api.dealer_helper import is_dealer_assigned, throw_number, update_all_bets
from api.exceptions import CasinoOutOfCash, GameNotFoundToPlay
from constant import SERVER_ERROR
from models import *

dealer = Blueprint("dealer", __name__, url_prefix="/dealer/v1")


@dealer.errorhandler(Exception)
def handle_500_error(_error):
    """Return a http 500 error to client"""
    print(_error)
    return make_response(jsonify(SERVER_ERROR), 500)


@dealer.route('/<dealer_id>/start_game', methods=["POST"])
def start_game(dealer_id):
    with LocalSession(Session) as session:
        if not is_dealer_assigned(dealer_id):
            game_obj = Game(dealer_id)
            session.add(game_obj)
            session.flush()
        else:
            return make_response(jsonify({
                'message': "failed",
                'data': {
                    'details': "Dealer is Already Assigned to a open game"
                }
            }), 400)
    return make_response(jsonify({
        'message': "success",
        'data': {
            'id': game_obj.id,
            'details': "Dealer has been assigned to new game"
        }
    }), 200)


@dealer.route('/<dealer_id>/stop_game', methods=["PUT"])
def stop_game(dealer_id):
    with LocalSession(Session) as session:
        filters = [Game.did == dealer_id, Game.status == GameStatus.OPEN.value]
        game_obj = session.query(Game).filter(and_(*filters)).first()
        if game_obj.id:
            game_obj.status = GameStatus.CLOSE.value
            session.flush()
        else:
            return make_response(jsonify({
                'message': "failed",
                'data': {
                    'details': "No open game assigned to dealer"
                }
            }), 400)
    return make_response(jsonify({
        'message': "success",
        'data': {
            'id': game_obj.id,
            'details': "Game has been closed"
        }
    }), 200)


@dealer.route('/<dealer_id>/play', methods=["GET"])
def settle_up_game(dealer_id):
    game_number = 13
    try:
        update_all_bets(dealer_id, game_number)
        return make_response(jsonify({
            'message': "success",
            'data': {
                'winning_number': game_number,
                'details': "Game has been Archived"
            }
        }), 200)
    except (CasinoOutOfCash, GameNotFoundToPlay) as ie:
        return make_response(jsonify({
            'message': "failed",
            'data': {
                'details': ie.message
            }
        }), 400)
