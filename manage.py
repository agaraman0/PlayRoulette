import os

from dotenv import load_dotenv, find_dotenv
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

from main import app
from db import *

load_dotenv(find_dotenv())


app.config.from_object(os.getenv('APP_SETTINGS'))

migrate = Migrate(app, db)
manager = Manager(app)

manager.add_command('db', MigrateCommand)


if __name__ == '__main__':
    manager.run()
