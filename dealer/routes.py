from flask import jsonify, Blueprint, make_response

from api_response import APIResponseClass, StatusMessage
from constant import SERVER_ERROR
from dealer.helpers import update_all_bets, create_game, stop_game_for_dealer, throw_number
from exceptions import CasinoOutOfCash, GameNotFoundToPlay, DealerAlreadyAssigned, DealerHasNoActiveGame

dealer = Blueprint("dealer", __name__, url_prefix="/dealer/v1")


@dealer.errorhandler(Exception)
def handle_500_error(_error):
    """Return a http 500 error to client"""
    return make_response(jsonify(SERVER_ERROR), 500)


@dealer.route('/<dealer_id>/start_game', methods=["POST"])
def start_game(dealer_id):
    api_response = APIResponseClass()
    try:
        api_response.data = create_game(dealer_id)
    except DealerAlreadyAssigned as ie:
        api_response.error = ie.message
        api_response.message = StatusMessage.FAILED
        api_response.status_code = 400
    return make_response(jsonify(api_response.get_response()), api_response.status_code)


@dealer.route('/<dealer_id>/stop_game', methods=["PUT"])
def stop_game(dealer_id):
    api_response = APIResponseClass()
    try:
        api_response.data = stop_game_for_dealer(dealer_id)
    except DealerHasNoActiveGame as ie:
        api_response.error = ie.message
        api_response.message = StatusMessage.FAILED
        api_response.status_code = 400
    return make_response(jsonify(api_response.get_response()), api_response.status_code)


@dealer.route('/<dealer_id>/play', methods=["GET"])
def settle_up_game(dealer_id):
    api_response = APIResponseClass()
    game_number = throw_number()
    try:
        api_response.data = update_all_bets(dealer_id, game_number)
    except (CasinoOutOfCash, GameNotFoundToPlay) as ie:
        api_response.error = ie.message
        api_response.message = StatusMessage.FAILED
        api_response.status_code = 400
    return make_response(jsonify(api_response.get_response()), api_response.status_code)
