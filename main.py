from flask import Flask
from api.casino import casino
from api.dealer import dealer
from api.user import user
from config import config
from db import db


app = Flask(__name__)
app.config.from_object(config)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db.init_app(app)
app.register_blueprint(casino)
app.register_blueprint(dealer)
app.register_blueprint(user)


@app.route('/<name>')
def hello_name(name):
    return "Hello {}!".format(name)


if __name__ == '__main__':
    app.run()
