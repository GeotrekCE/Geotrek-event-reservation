import pytest
import json
from flask import url_for, current_app
 
from app import create_app
from core.models import TTokens

@pytest.fixture()
def app():
    app = create_app()
    app.config.update({"TESTING": True})

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
    data = {"email": EMAIL}

    response = client.post(
        url_for("app_routes.send_login_email"), data=json.dumps(data), headers=headers
    )
    assert response.status_code == 204

    # Get token manually
    token = (
        TTokens.query.filter_by(used=False)
        .filter_by(email=EMAIL)
        .order_by(TTokens.created_at.desc())
        .first()
    )

    response = client.post(
        url_for("app_routes.login"),
        data=json.dumps({"login_token": token.token}),
        headers=headers,
    )
    assert response.status_code == 200
    rdata = json.loads(response.data)
    assert rdata["is_admin"] == True


def post_json(client, url, json_dict):
    """Send dictionary json_dict as a json to the specified url"""
    return client.post(url, data=json.dumps(json_dict), content_type="application/json")


def json_of_response(response):
    """Decode json from response"""
    return json.loads(response.data.decode("utf8"))
