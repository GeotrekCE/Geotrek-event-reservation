from flask import Flask, jsonify, request, current_app
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

from core.routes import app_routes
from core.env import db


# configuration
def create_app():
    # instantiate the app
    app = Flask(__name__)

    app.config.from_pyfile("./config/config.py")

    db.init_app(app)

    # enable CORS
    cors = CORS(app, resources={r"*": {"origins": "*"}}, supports_credentials=True)

    with app.app_context():
        # from pypnusershub import routes as fnauth

        # app.register_blueprint(fnauth.routes, url_prefix="/auth")
        app.register_blueprint(app_routes, url_prefix="/")

    return app
