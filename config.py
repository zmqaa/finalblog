import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = 'zmq'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR, 'data.sqlite')
    SQLALCHEMY_TRACK_MODIFICATIONS = False