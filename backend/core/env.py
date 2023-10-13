from os import environ

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
environ["FLASK_SQLALCHEMY_DB"] = f"{__name__}.db"
