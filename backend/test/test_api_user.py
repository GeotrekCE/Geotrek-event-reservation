from flask import url_for, current_app

import pytest
import json
import logging

from core.models import GTEvents, TReservations
from core.models import TTokens
from core.routes import EventIsFull

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


@pytest.mark.usefixtures("client_class")
class TestAPI:
    def test_post_reservation(self, events):
        login(self.client, "user@test.fr")
        # Create reservation
        event = (
            GTEvents.query.filter_by(name="Pytest bookable")
            .order_by(GTEvents.id.desc())
            .first()
        )

        data_resa = TEST_RESERVATION
        data_resa["id_event"] = event.id
        resp = post_json(
            self.client, url_for("app_routes.post_reservations"), data_resa
        )
        assert resp == 200

        # Confirm resa
        data = json.loads(resp.data)
        id_resa = data["id_reservation"]
        resa = TReservations.query.get(id_resa)
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
