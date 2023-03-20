import pytest
import json
from flask import url_for, current_app

from cookies import Cookie


from app import create_app
from config.conftest import LOGIN, PASSWORD, ID_APP


@pytest.fixture()
def app():
    app = create_app()
    app.config.update(
        {
            "TESTING": True,
            "LOGIN": LOGIN,
            "PASSWORD": PASSWORD,
            "ID_APP": ID_APP,
        }
    )

    # other setup can go here

    yield app

    # clean up / reset resources here


@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture()
def runner(app):
    return app.test_cli_runner()


mimetype = "application/json"
headers = {"Content-Type": mimetype, "Accept": mimetype}


def get_token(client):
    data = {
        "login": current_app.config.get("LOGIN"),
        "password": current_app.config.get("PASSWORD"),
        "id_app": current_app.config.get("ID_APP"),
    }

    response = client.post(
        url_for("auth.login"), data=json.dumps(data), headers=headers
    )
    try:
        token = Cookie.from_string(response.headers["Set-Cookie"])
        return token.value
    except Exception:
        raise Exception("Invalid login {}, {}".format(login, password))


def post_json(client, url, json_dict):
    """Send dictionary json_dict as a json to the specified url"""
    return client.post(url, data=json.dumps(json_dict), content_type="application/json")


def json_of_response(response):
    """Decode json from response"""
    return json.loads(response.data.decode("utf8"))
