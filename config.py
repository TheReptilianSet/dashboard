import os

BASE_DIR = os.path.dirname(__file__)


class Config:
    DEBUG = True
    SECRET_KEY = "82d9b4e1c4c432b0ec740f506353bea7b719c6659d19894ef3c3e612e44c3265"
    SQLALCHEMY_DATABASE_URI = "sqlite:///{}".format(os.path.join(BASE_DIR, "dash.db"))
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    SECURITY_PASSWORD_SALT = "bcrypt"