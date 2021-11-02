from flask import jsonify, Response, Blueprint, make_response
from models import *
from db import *

casino = Blueprint("crawler_extractor", __name__, url_prefix="/casino/v1")


@casino.route('/', methods=["GET"])
def hello():
    casinoObj = Casino("36 China Town")
    db.session.add(casinoObj)
    db.session.commit()
    return "Successful"
