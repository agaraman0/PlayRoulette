from flask import jsonify, Blueprint, make_response, request

from constant import SERVER_ERROR
from models import *

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
    with LocalSession(Session) as session:
        casino_obj = Casino(casino_name)
        session.add(casino_obj)
        session.flush()
    return make_response(jsonify({
        'message': "success",
        'data':  {
            'id': casino_obj.id
        }
    }), 200)


@casino.route('/<casino_id>/add_dealer', methods=["POST"])
def add_dealer(casino_id):
    json_args = request.json
    dealer_name = json_args.get('name')
    with LocalSession(Session) as session:
        dealer_obj = Dealer(dealer_name, casino_id)
        session.add(dealer_obj)
        session.flush()
    return make_response(jsonify({
        'message': "success",
        'data':  {
            'id': dealer_obj.id
        }
    }), 200)


@casino.route('/<casino_id>/dealers', methods=["GET"])
def list_dealers(casino_id):
    with LocalSession(Session) as session:
        df_response = session.query(Dealer).filter(Dealer.cid == casino_id).all()
        df_response = [dealer.get_format() for dealer in df_response]
    return make_response(jsonify({
        'message': "success",
        'data':  df_response
    }), 200)


@casino.route('/<casino_id>/recharge', methods=["PUT"])
def recharge_casino(casino_id):
    json_args = request.json
    amount = json_args.get('amount')
    with LocalSession(Session) as session:
        df_response = session.query(Casino).filter(Casino.id == casino_id).first()
        df_response.balance = amount
        session.flush()
    return make_response(jsonify({
        'message': "success",
        'data':  "{} Balance added to Casino named {}".format(amount, df_response.name)
    }), 200)
