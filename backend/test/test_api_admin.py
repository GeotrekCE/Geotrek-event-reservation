from flask import url_for, current_app

import csv
import pytest
import json
import logging

from io import StringIO

from sqlalchemy import select
from core.models import GTEvents, TReservations
from core.models import TTokens
from core.routes import EventIsFull
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
    "nom": "BLAIR",
    "prenom": "Eric",
    "commentaire": "saisie test",
    "tel": "00 00 00 00 00 ",
    "email": "maresa@test.fr",
    "nb_adultes": 1,
    "nb_moins_6_ans": 2,
    "nb_6_8_ans": 1,
    "nb_9_12_ans": 2,
    "nb_plus_12_ans": 2,
    "num_departement": "48",
    "confirmed": True,
}
TEST_BILAN = {
    "commentaire": "test bilan",
    "nb_6_8_ans": 1,
    "nb_9_12_ans": 2,
    "nb_adultes": 3,
    "nb_moins_6_ans": 6,
    "nb_plus_12_ans": 3,
}


@pytest.mark.usefixtures("client_class")
class TestAPI:
    def test_login(self):
        data = {"email": ADMIN_EMAIL}

        response = self.client.post(
            url_for("app_routes.send_login_email"),
            data=json.dumps(data),
            headers=headers,
        )
        assert response.status_code == 204

        # Get token manually
        token = db.session.scalars(
            select(TTokens)
            .where(TTokens.used == False, TTokens.email == ADMIN_EMAIL)
            .order_by(TTokens.created_at.desc())
        ).first()

        response = self.client.post(
            url_for("app_routes.login"),
            data=json.dumps({"login_token": token.token}),
            headers=headers,
        )
        assert response.status_code == 200
        rdata = json.loads(response.data)
        assert rdata["is_admin"] == True

    def test_get_events(self):
        response = self.client.get(url_for("app_routes.get_events"))
        assert response.status_code == 200
        response = self.client.get(
            url_for(
                "app_routes.get_events",
                published=True,
                begin_date="2023-06-27T22:00:00.000Z",
                end_date="2023-07-27T22:00:00.000Z",
                cancelled=True,
                sortBy="begin_date",
                sortDesc=False,
            )
        )
        assert response.status_code == 200

    def test_get_events_search_name(self, events):
        for search_name in ["ohoh", "öhôh"]:
            response = self.client.get(
                url_for("app_routes.get_events", search_name=search_name)
            )
            assert response.status_code == 200
            assert len(json.loads(response.data)["results"]) > 0

    def test_get_one_event(self, events):
        data = (
            db.session.execute(select(GTEvents).limit(1)).unique().scalar_one_or_none()
        )
        assert (
            self.client.get(
                url_for("app_routes.get_one_event", event_id=data.id)
            ).status_code
            == 200
        )

    def test_get_reservations(self):
        login(self.client)
        response = self.client.get(url_for("app_routes.get_reservations"))

        assert response.status_code == 200

    def test_post_reservation_isfull(self, events):
        login(self.client)
        # POST
        event = db.session.scalars(
            select(GTEvents)
            .where(GTEvents.name == "Pytest bookable")
            .order_by(GTEvents.id.desc())
            .limit(1)
        ).first()

        data_resa = TEST_RESERVATION
        data_resa["id_event"] = event.id
        resp = post_json(
            self.client, url_for("app_routes.post_reservations"), data_resa
        )
        assert resp == 200
        # Placement en liste d'attente
        resp = post_json(
            self.client, url_for("app_routes.post_reservations"), data_resa
        )
        assert resp == 200
        assert json_of_response(resp)["liste_attente"] == True

        # Refus de l'inscription
        resp = post_json(
            self.client, url_for("app_routes.post_reservations"), data_resa
        )
        assert resp.status_code == 422

    def test_post_reservation_notbookable(self, events):
        login(self.client)

        event = (
            db.session.execute(
                select(GTEvents).where(GTEvents.name == "Pytest not bookable").limit(1)
            )
            .unique()
            .scalar_one_or_none()
        )

        data_resa = TEST_RESERVATION
        data_resa["id_event"] = event.id
        resp = post_json(
            self.client, url_for("app_routes.post_reservations"), data_resa
        )

        assert resp.status_code == 422

    def test_post_export_and_cancel_one_reservation(self, events):
        login(self.client)
        # POST
        event = (
            db.session.execute(
                select(GTEvents)
                .where(GTEvents.name == "Pytest bookable")
                .order_by(GTEvents.id.desc())
                .limit(1)
            )
            .unique()
            .scalar_one_or_none()
        )

        data_resa = TEST_RESERVATION
        data_resa["id_event"] = event.id
        resp = post_json(
            self.client, url_for("app_routes.post_reservations"), data_resa
        )
        assert resp == 200
        resa_resp = json_of_response(resp)
        id_reservation = resa_resp["id_reservation"]

        resa = db.session.get(TReservations, id_reservation)

        # Check is confirm
        assert resa.confirmed == True

        # EXPORT liste participants
        resp = self.client.get(
            url_for("app_routes.export_reservation", id=resa.id_event)
        )
        assert resp.status_code == 200
        assert (
            f"export_reservation_{resa.id_event}.csv"
            in resp.headers["Content-Disposition"]
        )

        content = resp.data.decode("utf-8")
        cvs_reader = csv.reader(StringIO(content), delimiter=";")
        body = list(cvs_reader)
        headers = body.pop(0)
        assert len(body) == 1
        assert headers == [
            "id_reservation",
            "id_event",
            "Nom",
            "Prénom",
            "Email",
            "Téléphone",
            "Sur liste attente",
            "Nombre participants",
            "Nombre participants sur liste d’attente",
            "Nb adultes",
            "Nb enfants moins de 6 ans",
            "Nb enfants 6-8 ans",
            "Nb enfants 9-12 ans",
            "Nb enfants plus de 12 ans",
            "Département",
            "Commentaire",
        ]

        # Cancel
        # resa = TReservations.query.limit(1).one()

        response = self.client.delete(
            url_for("app_routes.cancel_reservation", reservation_id=id_reservation)
        )
        assert response.status_code == 204

        resa = db.session.get(TReservations, id_reservation)
        assert resa.cancelled == True
        assert resa.cancel_by == "admin"

    # def test_post_one_bilan(self):
    #     # POST
    #     event = GTEvents.query.limit(1).one()
    #     data_bilan = TEST_BILAN
    #     data_bilan["id_event"] = event.id
    #     resp = post_json(self.client, url_for("app_routes.post_bilans"), data_bilan)
    #     assert resp == 200

    def test_bilan_global(self):
        login(self.client)
        donnees_exemple = {
            "nb_animations": 1,
            "nb_annulation": 0,
            "sum_nb_inscriptions": 2,
            "sum_nb_participants_possible": 2089,
            "taux_remplissage": 0.0007017543859649122,
            "taux_remplissage_passe": 0.0007017543859649122,
        }
        response = self.client.get(url_for("app_routes.get_stats_global"))
        assert response.status_code == 200

        data = json_of_response(response)

        assert set(data.keys()) == set(donnees_exemple.keys())
        # Todo test return value

        response = self.client.get(url_for("app_routes.get_stats_global", year="2023"))
        assert response.status_code == 200

    def test_export_global(self):
        login(self.client)
        response = self.client.get(url_for("app_routes.get_export_events"))
        assert response.status_code == 200

        #  test response
        exported_columns = [
            "id",
            "zoning_city",
            "zoning_district",
            "name_fr",
            "type",
            "begin_date",
            "end_date",
            "capacity",
            "target_audience",
            "resa_nb_total",
            "resa_nb_total_attente",
            "annulation",
            "categorie_annulation",
            "raison_annulation",
            "bilan_nb_adultes",
            "bilan_nb_moins_6_ans",
            "bilan_nb_6_8_ans",
            "bilan_nb_9_12_ans",
            "bilan_nb_plus_12_ans",
            "bilan_commentaire",
            "resa_nb_adultes",
            "resa_nb_moins_6_ans",
            "resa_nb_6_8_ans",
            "resa_nb_nb_9_12_ans",
            "resa_nb_plus_12_ans",
            "resa_nb_adultes_attente",
            "resa_nb_moins_6_ans_attente",
            "resa_nb_6_8_ans_attente",
            "resa_nb_9_12_ans_attente",
            "resa_nb_plus_12_ans_attente",
            "published",
        ]

        csv_data = response.data.decode("utf8")
        with StringIO(csv_data) as f:
            cvs_reader = csv.DictReader(f, delimiter=";")
            assert cvs_reader.fieldnames == exported_columns

    def test_get_event_info(self):
        login(self.client)
        data = db.session.scalars(select(GTEvents)).first()
        response = self.client.get(
            url_for("app_routes.get_event_info", event_id=data.id)
        )
        assert response.status_code == 200
