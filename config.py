import os


basedir = os.path.abspath(os.path.dirname(__file__))

os.environ['DATABASE_URL'] = "postgresql://aman:aman@db:5432/aman"
os.environ['FLASK_APP'] = "main.py"


class Config(object):
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']


class ProductionConfig(Config):
    DEBUG = False


class StagingConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class TestingConfig(Config):
    TESTING = True


config = ProductionConfig()
config_str = os.getenv('SRC_ENV', 'prod')
if config_str == 'dev':
    config = DevelopmentConfig()
elif config_str == 'test':
    config = TestingConfig()
else:
    config = ProductionConfig()
