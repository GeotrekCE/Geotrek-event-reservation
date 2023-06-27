import pytest
import json

from datetime import date
from flask import url_for
from sqlalchemy.sql import text
from app import create_app

from core.models import TTokens, GTEvents
from core.env import db


headers = {"Content-type": "application/json", "Accept": "application/json"}

events_data = [
    {
        # id:
        "name": "Pytest",
        "capacity": 10,
        "begin_date": "01/07/2023",
        "end_date": "01/10/2023",
        "published": True,
        "x": 765227.4922990737,
        "y": 6365673.938623513,
        "published_fr": True,
        "published_en": True,
    }
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
    token = (
        TTokens.query.filter_by(used=False)
        .filter_by(email=ADMIN_EMAIL)
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


@pytest.fixture(scope="function")
def events():
    with db.session.begin_nested():
        for e in events_data:
            # Fait en sql direct pour éviter de réaliser un mapping complet
            #  du model tourism_touristicevent et notamment le champ géométrie
            db.session.execute(
                text(
                    """
                INSERT INTO public.tourism_touristicevent
                (
                  date_insert, date_update, deleted, structure_id,
                  geom,published,"name",capacity, begin_date, end_date,
                  published_fr, published_en
                )
                VALUES (CURRENT_TIMESTAMP,CURRENT_TIMESTAMP, false, 1,
                 st_setsrid(st_point(:x, :y), 2154), :published, :name, :capacity,:begin_date , :end_date ,
                 :published_fr, :published_en
                 )
                """
                ),
                params=e,
            )
