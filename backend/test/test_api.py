from flask import url_for, current_app
from .conftest import get_token, json_of_response, post_json
import pytest
import json
import logging

from core.models import GTEvents, TReservations, TAnimationsBilans

LOGGER = logging.getLogger(__name__)


TEST_RESERVATION = {
  "nom":"BLAIR",
  "prenom":"Eric",
  "commentaire":"saisie test",
  "liste_attente":True,
  "nb_adultes":1,
  "nb_moins_6_ans":2,
  "nb_6_8_ans":1,
  "nb_9_12_ans":2,
  "nb_plus_12_ans":2,
  "tel":"00 00 00 00 00 ",
  "num_departement":"Lozère",
  "commentaire_numerisateur":"saisietest",
}
TEST_BILAN = {
  "commentaire": "test bilan",
  "nb_6_8_ans": 1,
  "nb_9_12_ans": 2,
  "nb_adultes": 3,
  "nb_moins_6_ans": 6,
  "nb_plus_12_ans": 3,
}

@pytest.mark.usefixtures('client_class')
class TestAPI:
  def test_get_events(self):
    token = get_token(self.client)
    self.client.set_cookie("/", "token", token)
    response =  self.client.get(url_for("app_routes.get_events"))
    assert response.status_code == 200


  def test_get_one_event(self):
    token = get_token(self.client)
    self.client.set_cookie("/", "token", token)
    data = GTEvents.query.limit(1).one()
    assert self.client.get(url_for("app_routes.get_one_event", id=data.id)).status_code == 200


  def test_post_export_and_delete_one_reservation(self):
    token = get_token(self.client)
    self.client.set_cookie("/", "token", token)
    # POST
    event = GTEvents.query.limit(1).one()
    data_resa = TEST_RESERVATION
    data_resa["id_event"] = event.id
    resp = post_json(self.client, url_for("app_routes.post_reservations"), data_resa)
    assert resp == 200
    # EXPORT
    self.client.set_cookie("/", "token", token)
    resa = TReservations.query.limit(1).one()
    resp = self.client.get(
      url_for("app_routes.export_reservation", id=resa.id_event)
    )
    assert resp.status_code == 200
    assert f"export_reservation_{resa.id_event}.csv" in resp.headers["Content-Disposition"]

    # DELETE
    self.client.set_cookie("/", "token", token)
    resa = TReservations.query.limit(1).one()
    assert self.client.delete(url_for("app_routes.delete_reservations", id_reservation=resa.id_reservation)).status_code == 200


  def test_post_one_bilan(self):
    token = get_token(self.client)
    self.client.set_cookie("/", "token", token)
    # POST
    event = GTEvents.query.limit(1).one()
    data_bilan = TEST_BILAN
    data_bilan["id_event"] = event.id
    resp = post_json(self.client, url_for("app_routes.post_bilans"), data_bilan)
    assert resp == 200
