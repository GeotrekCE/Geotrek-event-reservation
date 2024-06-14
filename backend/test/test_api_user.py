from flask import url_for, current_app

import pytest
import json
import logging

from sqlalchemy import select

from core.models import GTEvents, TReservations
from core.models import TTokens
from core.exceptions import EventIsFull
from core.env import db

from .utils import login
from .fixtures import (
    events,
    ADMIN_EMAIL,
    get_token,
    json_of_response,
    post_json,
    app,
    headers,
)

LOGGER = logging.getLogger(__name__)


TEST_RESERVATION = {
    "nom": "YO",
    "prenom": "yo",
    "commentaire": "saisie test",
    "tel": "00 00 00 00 00 ",
    "email": "user@test.fr",
    "nb_adultes": 1,
    "nb_moins_6_ans": 2,
    "nb_6_8_ans": 1,
    "nb_9_12_ans": 2,
    "nb_plus_12_ans": 2,
    "num_departement": "48",
}

TEST_RESERVATION_1_PERSONNE = {
    "nom": "YO",
    "prenom": "yo",
    "commentaire": "saisie test",
    "tel": "00 00 00 00 00 ",
    "email": "user.tropresa@test.fr",
    "nb_adultes": 1,
    "nb_moins_6_ans": 0,
    "nb_6_8_ans": 0,
    "nb_9_12_ans": 0,
    "nb_plus_12_ans": 0,
    "num_departement": "48",
}

TEST_RESERVATION_PLEIN_PERSONNES = {
    "nom": "YO",
    "prenom": "yo",
    "commentaire": "saisie test",
    "tel": "00 00 00 00 00 ",
    "email": "user.tropmonde@test.fr",
    "nb_adultes": 10,
    "nb_moins_6_ans": 10,
    "nb_6_8_ans": 10,
    "nb_9_12_ans": 10,
    "nb_plus_12_ans": 0,
    "num_departement": "48",
}

@pytest.mark.usefixtures("client_class")
class TestAPI:
    def test_post_reservation(self, events):
        login(self.client, "user@test.fr")
        # Create reservation
        event = db.session.scalars(
            select(GTEvents)
            .where(GTEvents.name == "Pytest bookable")
            .order_by(GTEvents.id.desc())
        ).first()

        data_resa = TEST_RESERVATION
        data_resa["id_event"] = event.id
        resp = post_json(
            self.client, url_for("app_routes.post_reservations"), data_resa
        )
        assert resp == 200

        # Confirm resa
        data = json.loads(resp.data)
        id_resa = data["id_reservation"]
        resa = db.session.get(TReservations, id_resa)
        resp = post_json(
            self.client,
            url_for("app_routes.confirm_reservation"),
            {"resa_token": resa.token},
        )
        assert resp == 200

        # Already confirmed
        resp = post_json(
            self.client,
            url_for("app_routes.confirm_reservation"),
            {"resa_token": resa.token},
        )
        assert resp == 400

        # Cancel reservation
        resp = self.client.delete(
            url_for("app_routes.cancel_reservation", reservation_id=id_resa)
        )
        assert resp == 204

        # Already canceled reservation
        resp = self.client.delete(
            url_for("app_routes.cancel_reservation", reservation_id=id_resa)
        )
        assert resp == 400

    def test_get_reservations(self):
        login(self.client, "user@test.fr")
        response = self.client.get(url_for("app_routes.get_reservations"))

        assert response.status_code == 200

    def test_post_limit_nb_animations(self, events):
        login(self.client, "user@test.fr")
        # Create reservation
        event = db.session.scalars(
            select(GTEvents)
            .where(GTEvents.name == "Pytest bookable")
            .order_by(GTEvents.id.desc())
        ).first()

        data_resa = TEST_RESERVATION_1_PERSONNE
        data_resa["id_event"] = event.id

        nb_limit_per_user = current_app.config["NB_ANIM_MAX_PER_USER"]

        # Création du nombre de reservations spécifiée dans NB_ANIM_MAX_PER_USER

        for loop in range(nb_limit_per_user):
            resp = post_json(
                self.client, url_for("app_routes.post_reservations"), data_resa
            )
            assert resp == 200
            # Confirm resa
            data = json.loads(resp.data)
            id_resa = data["id_reservation"]
            resa = db.session.get(TReservations, id_resa)
            resp = post_json(
                self.client,
                url_for("app_routes.confirm_reservation"),
                {"resa_token": resa.token},
            )
            assert resp == 200

        #  Ajout de 1 reservation ce qui doit retourner une erreur
        resp = post_json(
            self.client, url_for("app_routes.post_reservations"), data_resa
        )
        assert resp.status_code == 422
        assert (
            json_of_response(resp)["error"]
            == "Vous avez atteind la limite du nombre de réservation possible par personne"
        )

    def test_post_limit_nb_participants(self, events):
        login(self.client, "user@test.fr")
        # Create reservation
        event = db.session.scalars(
            select(GTEvents)
            .where(GTEvents.name == "Pytest bookable")
            .order_by(GTEvents.id.desc())
        ).first()

        data_resa = TEST_RESERVATION_PLEIN_PERSONNES
        data_resa["id_event"] = event.id

        resp = post_json(
            self.client, url_for("app_routes.post_reservations"), data_resa
        )
        assert resp.status_code == 422
        assert (
            json_of_response(resp)["error"]
            == "Vous avez ne pouvez pas inscrire autant de personne sur une animation"
        )
