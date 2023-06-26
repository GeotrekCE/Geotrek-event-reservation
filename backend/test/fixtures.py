import pytest
from datetime import date
from flask import url_for
from sqlalchemy.sql import text
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
        "published_en" : True
    }
]


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
