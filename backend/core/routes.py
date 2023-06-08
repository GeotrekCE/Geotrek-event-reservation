import secrets

from email_validator import validate_email, EmailNotValidError, EmailSyntaxError
from flask import jsonify, request, Blueprint, render_template, session
from flask_mail import Message

from core.models import db, GTEvents, TReservations, VExportBilan, TTokens
from core.repository import query_stats_bilan, query_stats_animations_per_month
from core.schemas import (
    GTEventsSchema,
    TReservationsSchema,
    TAnimationsBilansSchema,
    VExportBilanSchema,
)
from core.utils import to_csv_resp, transform_obj_to_flat_list


app_routes = Blueprint("app_routes", __name__)


def send_email(subject, recipients, html):
    msg = Message(subject=subject, recipients=recipients, html=html)
    print("email sent", msg)
    from app import mail
    mail.send(msg)


def generate_token():
    return secrets.token_hex(16)


def get_confirmation_link(reservation):
    from flask import current_app
    protocol = "http://" if current_app.config["DEBUG"] else "https://"
    hostname = current_app.config["SERVER_NAME"]
    front_path = current_app.config["FRONTEND_PATHNAME"]
    return f"{protocol}{hostname}{front_path}?token={reservation.token}"


def get_login_link(token):
    from flask import current_app
    protocol = "http://" if current_app.config["DEBUG"] else "https://"
    hostname = current_app.config["SERVER_NAME"]
    front_path = current_app.config["FRONTEND_LOGIN_PATHNAME"]
    return f"{protocol}{hostname}{front_path}?token={token}"


@app_routes.route("/events")
def get_events():
    page = request.args.get("page", 1, type=int)
    limit = request.args.get("limit", 10, type=int)

    if "fields" in request.args:
        fields = request.args.getlist("fields", None)
        fields = fields[0].split(",") + fields[1:]
    else:
        fields = None

    query_params = request.args.to_dict()

    # Clean query params
    for p in ("limit", "page", "fields"):
        if query_params.get(p, None):
            query_params.pop(p)

    # Ordonancement
    sort_col = "begin_date"
    if "sortBy" in request.args:
        sort_col = query_params.pop("sortBy")

    sort_order = "desc"
    try:
        sort_order_param = query_params.pop("sortDesc")
        if sort_order_param == "false":
            sort_order = "asc"
    except KeyError:
        sort_order = "desc"

    events = GTEvents.query.filter_properties(query_params)
    if hasattr(GTEvents, sort_col):
        model_sort_col = getattr(GTEvents, sort_col)
    else:
        model_sort_col = GTEvents.begin_date

    events = events.order_by(getattr(model_sort_col, sort_order)(), GTEvents.id.asc())

    events = events.paginate(page=page, per_page=limit)

    results = GTEventsSchema(many=True, only=fields).dump(events.items)

    return jsonify(
        {
            "page": page,
            "limit": limit,
            "total": events.total,
            "has_next": events.has_next,
            "has_prev": events.has_prev,
            "results": results,
        }
    )


@app_routes.route("/events/<id>")
def get_one_event(id):
    events = GTEvents.query.get_or_404(id)
    results = GTEventsSchema().dump(events)
    return jsonify(results)


@app_routes.route("/reservations", methods=["POST"])
def post_reservations():
    post_data = request.get_json()

    reservation = TReservationsSchema().load(post_data, session=db.session)
    reservation.token = generate_token()

    db.session.add(reservation)
    db.session.commit()
    # db.session.close()

    send_email(
        subject="Lien pour confirmer votre demande de réservation",
        recipients=[reservation.email],
        html=render_template(
            "please_confirm_resa_mail.html",
            confirmation_link=get_confirmation_link(reservation),
            event=reservation.event.name
        )
    )

    return jsonify({"msg": "Demande de réservation enregistrée"})


@app_routes.route("/reservations/confirm", methods=["POST"])
def confirm_reservation():
    """Expects the reservation's token in the request body as JSON: {"resa_token": "12345abcde"}, if the corresponding
    reservation exists it is confirmed and a confirmation mail is sent."""
    token = request.get_json()["resa_token"]
    resa = db.first_or_404(db.select(TReservations).filter_by(token=token), description="Reservation not found")
    if resa.confirmed:
        return "Reservation already confirmed", 400
    resa.confirmed = True
    db.session.add(resa)
    db.session.commit()

    send_email(
        subject="Votre réservation est confirmée",
        recipients=[resa.email],
        html=render_template(
            "resa_confirmed_mail.html",
            nb_places=resa.nb_participants,
            event="la super fête"
        )
    )

    return "", 204


@app_routes.route("/send-login-email", methods=["POST"])
def send_login_email():
    try:
        email = request.get_json()["email"]
    except KeyError:
        return "'email' property is mandatory", 400

    try:
        email_info = validate_email(email, check_deliverability=False)
    except (EmailNotValidError, EmailSyntaxError) as e:
        return f"email is not valid: {e}", 400
    clean_email = email_info.normalized

    token = TTokens(email=clean_email, token=generate_token())

    db.session.add(token)
    db.session.save()

    send_email(
        "Lien de connexion sur site de réservation du PNG",
        recipients=[email],
        html=render_template(
            "login_mail.html",
            confirmation_link=get_login_link(token)
        )
    )

    return "lien de login envoyé", 204


@app_routes.route("/login", methods=["POST"])
def login():
    try:
        login_token = request.json["login_token"]
    except KeyError:
        return "Expects a JSON body with a 'login_token' property", 400

    # TODO: handle token expiration
    token = db.first_or_404(db.select(TTokens).filter_by(token=login_token), description="The login token is invalid or expired")

    # Set a Session Cookie in the response.
    session['user'] = token.email

    return "login successful", 200


@app_routes.route("/export_reservation/<id>", methods=["GET"])
#@fnauth.check_auth(1)
def export_reservation(id):
    resa = TReservations.query.filter_by(id_event=id).all()

    results = TReservationsSchema(many=True).dump(resa)
    export_fields = [
        "id_reservation",
        "id_event",
        "nom",
        "prenom",
        "tel",
        "liste_attente",
        "sum_participants",
        "sum_participants_liste_attente",
        "nb_adultes",
        "nb_moins_6_ans",
        "nb_6_8_ans",
        "nb_9_12_ans",
        "nb_plus_12_ans",
        "num_departement",
        # "numerisateur.identifiant",
        "id_numerisateur",
        "commentaire_numerisateur",
        "commentaire",
        "meta_create_date",
        "meta_update_date",
    ]
    data = transform_obj_to_flat_list(export_fields, results)
    return to_csv_resp(f"reservation_{id}", data, export_fields, ";")


@app_routes.route("/bilans", methods=["POST"])
#@fnauth.check_auth(1)
def post_bilans():
    post_data = request.get_json()
    bilan = TAnimationsBilansSchema().load(post_data, session=db.session)

    db.session.add(bilan)
    db.session.commit()
    db.session.close()
    return jsonify({"msg": "Données sauvegardées"})


@app_routes.route("/reservations/<id_reservation>", methods=["DELETE"])
#@fnauth.check_auth(1)
def delete_reservations(id_reservation):
    reservation = TReservations.query.get_or_404(id_reservation)
    db.session.delete(reservation)
    db.session.commit()
    return jsonify({"msg": "Données supprimées"})


@app_routes.route("/stats/global", methods=["GET"])
#@fnauth.check_auth(1)
def get_stats_global():
    params = request.args
    data = query_stats_bilan(params)

    return jsonify(data)


@app_routes.route("/stats/charts/nb_day_before_resa", methods=["GET"])
#@fnauth.check_auth(1)
def get_stats_nb_day_before_resa():
    params = request.args
    data = query_stats_animations_per_month(params)
    return jsonify(data)


@app_routes.route("/export/events")
#@fnauth.check_auth(1)
def get_export_events():
    events = VExportBilan.query.all()
    results = VExportBilanSchema(many=True).dump(events)
    fields = VExportBilan.__table__.columns.keys()
    return to_csv_resp("export_bilan", results, fields, ";")
