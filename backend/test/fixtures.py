import pytest
import json


from datetime import date, datetime, timedelta
from flask import url_for
from sqlalchemy import select
from sqlalchemy.sql import text
from geoalchemy2.shape import from_shape
from shapely.geometry import Point
from app import create_app

from core.models import TTokens, GTEvents
from core.env import db

headers = {"Content-type": "application/json", "Accept": "application/json"}

events_data = [
    {
        # id:
        "name": "Pytest bookable",
        "capacity": 10,
        "begin_date": datetime.today().date() + timedelta(6 * 30),
        "end_date": datetime.today().date() + timedelta(6 * 30),
        "published": True,
        "published_fr": True,
        "published_en": True,
        "bookable": True,
        "eid": "0",
    },
    {
        # id:
        "name": "Pytest not bookable",
        "capacity": None,
        "begin_date": datetime.today().date(),
        "end_date": datetime.today().date(),
        "published": True,
        "published_fr": True,
        "published_en": True,
        "bookable": False,
        "eid": "0",
    },
    {
        # id:
        "name": "Pytest avec accents àeù öhôh",
        "capacity": None,
        "begin_date": datetime.today().date(),
        "end_date": datetime.today().date(),
        "published": True,
        "published_fr": True,
        "published_en": True,
        "bookable": False,
        "eid": "0",
    },
    {
        # id:
        "name": "Pytest past",
        "capacity": None,
        "begin_date": "01/07/2023",
        "end_date": "01/10/2023",
        "published": True,
        "published_fr": True,
        "published_en": True,
        "bookable": True,
        "eid": "0",
    },
]


ADMIN_EMAIL = "test.test@test.fr"


@pytest.fixture()
def app():
    app = create_app()
    app.config.update({"TESTING": True, "ADMIN_EMAILS": [ADMIN_EMAIL]})

    # other setup can go here

    yield app

    # clean up / reset resources here


@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture()
def runner(app):
    return app.test_cli_runner()


def get_token(client):
    data = {"email": ADMIN_EMAIL}

    response = client.post(
        url_for("app_routes.send_login_email"), data=json.dumps(data), headers=headers
    )
    assert response.status_code == 204

    # Get token manually
    token = db.session.scalars(
        select(TTokens)
        .where(TTokens.used == False, TTokens.email == ADMIN_EMAIL)
        .order_by(TTokens.created_at.desc())
    ).first()

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
    return client.post(url, json=json_dict, content_type="application/json")


def json_of_response(response):
    """Decode json from response"""
    return json.loads(response.data.decode("utf8"))


@pytest.fixture(scope="function")
def events():
    events_list = {}
    with db.session.begin_nested():
        for e in events_data:
            geom = from_shape(Point(765227.4922990737, 6365673.938623513), srid=2154)
            e["geom"] = geom
            event = GTEvents(**e)
            db.session.add(event)
            events_list[e["name"]] = event
    return events_list
