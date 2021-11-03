from flask import jsonify, Blueprint, make_response, request

from casino.helpers import register_casino, add_dealer_to_casino, list_all_dealers, add_balance_to_casino
from constant import SERVER_ERROR

casino = Blueprint("casino", __name__, url_prefix="/casino/v1")


@casino.errorhandler(Exception)
def handle_500_error(_error):
    """Return a http 500 error to client"""
    print(_error)
    return make_response(jsonify(SERVER_ERROR), 500)


@casino.route('/create_casino', methods=["POST"])
def hello():
    json_args = request.json
    casino_name = json_args.get('name')
    casino_id = register_casino(casino_name)
    return make_response(jsonify({
        'message': "success",
        'data':  {
            'id': casino_id
        }
    }), 200)


@casino.route('/<casino_id>/add_dealer', methods=["POST"])
def add_dealer(casino_id):
    json_args = request.json
    dealer_name = json_args.get('name')
    dealer_id = add_dealer_to_casino(casino_id, dealer_name)
    return make_response(jsonify({
        'message': "success",
        'data':  {
            'id': dealer_id
        }
    }), 200)


@casino.route('/<casino_id>/dealers', methods=["GET"])
def list_dealers(casino_id):
    df_response = list_all_dealers(casino_id)
    return make_response(jsonify({
        'message': "success",
        'data':  df_response
    }), 200)


@casino.route('/<casino_id>/recharge', methods=["PUT"])
def recharge_casino(casino_id):
    json_args = request.json
    amount = json_args.get('amount')
    casino_obj = add_balance_to_casino(casino_id, amount)
    return make_response(jsonify({
        'message': "success",
        'data':  "{} New Balance of Casino {} with id {}".format(casino_obj.balance, casino_obj.name, casino_obj.id)
    }), 200)
