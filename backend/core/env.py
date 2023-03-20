from os import environ
from importlib import import_module

from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()
environ["FLASK_SQLALCHEMY_DB"] = f"{__name__}.db"
