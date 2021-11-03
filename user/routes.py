from flask import jsonify, Blueprint, make_response, request

from helpers.api_response import APIResponseClass, StatusMessage
from helpers.constant import SERVER_ERROR
from helpers.exceptions import *
from user.helpers import create_user, assign_casino, \
    list_all_games, add_amount_to_user_balance, user_balance, make_bet

user = Blueprint("user", __name__, url_prefix="/user/v1")


@user.errorhandler(Exception)
def handle_500_error(_error):
    """Return a http 500 error to client"""
    return make_response(jsonify(SERVER_ERROR), 500)


@user.route('/register', methods=["POST"])
def register_user():
    api_response = APIResponseClass()
    json_args = request.json
    user_name = json_args.get('name')
    api_response.data = create_user(user_name)
    return make_response(jsonify(api_response.get_response()), api_response.status_code)


@user.route('/<user_id>/enter_casino', methods=["PUT"])
def enter_casino(user_id):
    api_response = APIResponseClass()
    json_args = request.json
    casino_id = json_args.get('casino_id')
    try:
        api_response.data = assign_casino(casino_id, user_id)
    except CasinoNotFound as ie:
        api_response.error = ie.message
        api_response.message = StatusMessage.FAILED
        api_response.status_code = 400
    return make_response(jsonify(api_response.get_response()), api_response.status_code)


@user.route('/<user_id>/recharge', methods=["PUT"])
def recharge_user_balance(user_id):
    api_response = APIResponseClass()
    json_args = request.json
    amount = json_args.get('amount')
    try:
        api_response.data = add_amount_to_user_balance(user_id, amount)
    except InsufficientAmount as ie:
        api_response.error = ie.message
        api_response.message = StatusMessage.FAILED
        api_response.status_code = 400
    return make_response(jsonify(api_response.get_response()), api_response.status_code)


@user.route('/<user_id>/cashout', methods=['GET'])
def get_user_balance(user_id):
    api_response = APIResponseClass()
    try:
        api_response.data = user_balance(user_id)
    except UserNotFound as ie:
        api_response.error = ie.message
        api_response.message = StatusMessage.FAILED
        api_response.status_code = 400
    return make_response(jsonify(api_response.get_response()), api_response.status_code)


@user.route('/<user_id>/games_available', methods=['GET'])
def get_available_games(user_id):
    api_response = APIResponseClass()
    try:
        api_response.data = list_all_games(user_id)
    except UserNotFound as ie:
        api_response.message = StatusMessage.FAILED
        api_response.error = ie.message
        api_response.status_code = 400
    return make_response(jsonify(api_response.get_response()), api_response.status_code)


@user.route('/<user_id>/bet', methods=['POST'])
def bet_on_game(user_id):
    api_response = APIResponseClass()
    json_args = request.json
    bet_number = json_args.get('lucky_number')
    bet_amount = json_args.get('amount')
    game_id = json_args.get('game_id')
    try:
        api_response.data = make_bet(user_id, bet_amount, game_id, bet_number)
    except (InsufficientAmount, GameNotAvailableForUser, NumberOutOfRange) as ie:
        api_response.error = ie.message
        api_response.message = StatusMessage.FAILED
        api_response.status_code = 400
    return make_response(jsonify(api_response.get_response()), api_response.status_code)
