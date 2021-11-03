from flask import jsonify, Blueprint, make_response, request

from helpers.api_response import APIResponseClass
from casino.helpers import register_casino, add_dealer_to_casino, list_all_dealers, add_balance_to_casino
from helpers.constant import SERVER_ERROR

casino = Blueprint("casino", __name__, url_prefix="/casino/v1")


@casino.errorhandler(Exception)
def handle_500_error(_error):
    """Return a http 500 error to client"""
    print(_error)
    return make_response(jsonify(SERVER_ERROR), 500)


@casino.route('/create_casino', methods=["POST"])
def create_casino():
    api_response = APIResponseClass()
    json_args = request.json
    casino_name = json_args.get('name')
    casino_id = register_casino(casino_name)
    api_response.data = casino_id
    return make_response(jsonify(api_response.get_response()), api_response.status_code)


@casino.route('/<casino_id>/add_dealer', methods=["POST"])
def add_dealer(casino_id):
    api_response = APIResponseClass()
    json_args = request.json
    dealer_name = json_args.get('name')
    api_response.data = add_dealer_to_casino(casino_id, dealer_name)
    return make_response(jsonify(api_response.get_response()), api_response.status_code)


@casino.route('/<casino_id>/dealers', methods=["GET"])
def list_dealers(casino_id):
    api_response = APIResponseClass()
    api_response.data = list_all_dealers(casino_id)
    return make_response(jsonify(api_response.get_response()), api_response.status_code)


@casino.route('/<casino_id>/recharge', methods=["PUT"])
def recharge_casino(casino_id):
    api_response = APIResponseClass()
    json_args = request.json
    amount = json_args.get('amount')
    api_response.data = add_balance_to_casino(casino_id, amount)
    return make_response(jsonify(api_response.get_response()), api_response.status_code)
