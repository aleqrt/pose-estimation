import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    CORS_HEADERS = os.environ.get('CORS_HEADERS') or 'Content-Type'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'db_model',
                                                                                            'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
