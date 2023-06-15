import email_validator
from flask import Flask, jsonify
from flask_cors import CORS
from flask_mail import Mail
from marshmallow.exceptions import ValidationError as MarshmallowValidationError

from core.env import db
from core.routes import app_routes, QueryParamValidationError

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

    @app.errorhandler(MarshmallowValidationError)
    def handle_bad_request(e):
        return jsonify({"error": str(e)}), 400

    @app.errorhandler(QueryParamValidationError)
    def handle_bad_request(e):
        return jsonify({"error": str(e)}), 400

    return app
