import email_validator
from flask import Flask
from flask_cors import CORS
from flask_mail import Mail
from marshmallow.exceptions import ValidationError

from core.env import db
from core.routes import app_routes

mail = None


# configuration
def create_app():
    # instantiate the app
    app = Flask(__name__)

    app.config.from_pyfile("./config/config.py")
    if app.config["DEBUG"] or app.config["TESTING"]:
        email_validator.TEST_ENVIRONMENT = True

    db.init_app(app)

    # enable CORS
    cors = CORS(app, resources={r"*": {"origins": "*"}}, supports_credentials=True)

    with app.app_context():
        app.register_blueprint(app_routes, url_prefix="/")

    global mail
    mail = Mail(app)

    @app.errorhandler(ValidationError)
    def handle_bad_request(e):
        return str(e), 400

    return app
