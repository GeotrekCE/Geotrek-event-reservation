import logging

from babel.dates import format_date as babel_format_date, format_time as babel_format_time
import email_validator
from flask import Flask, jsonify
from flask_cors import CORS
from flask_mail import Mail
from marshmallow.exceptions import ValidationError as MarshmallowValidationError

from core.env import db
from core.routes import app_routes, QueryParamValidationError, EventIsFull

mail = None


# configuration
def create_app():
    # instantiate the app
    app = Flask(__name__)

    app.config.from_pyfile("./config/config.py")
    if app.config["DEBUG"] or app.config["TESTING"]:
        email_validator.TEST_ENVIRONMENT = True

    logging.config.dictConfig(app.config["LOGGING"])

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
    def handle_bad_query_param_error(e):
        return jsonify({"error": str(e)}), 400

    @app.errorhandler(EventIsFull)
    def handle_event_is_full_error(e):
        return jsonify({"error": "Réservation ou placement sur liste d'attente impossible, l'événement est complet"}), 422

    @app.template_filter()
    def format_date(value):
        format_string = "EEEE d MMMM"
        if not value or value == "--":
            return ""
        return babel_format_date(value, format_string, locale="fr_FR")

    @app.template_filter()
    def format_time(value):
        format_string = "H'h'mm"
        if not value or value == "--":
            return ""
        return babel_format_time(value, format_string, locale="fr_FR")

    return app
