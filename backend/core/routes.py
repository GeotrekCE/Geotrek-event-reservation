from datetime import datetime
from functools import wraps
import secrets

from email_validator import validate_email, EmailNotValidError, EmailSyntaxError
from flask import jsonify, request, Blueprint, render_template, session, current_app
from flask_mail import Message

from core.models import db, GTEvents, TReservations, VExportBilan, TTokens
from core.repository import query_stats_bilan, query_stats_animations_per_month
from core.schemas import (
    GTEventsSchema,
    TReservationsSchema,
    TReservationsUpdateSchema,
    TAnimationsBilansSchema,
    VExportBilanSchema,
)
from core.utils import to_csv_resp, transform_obj_to_flat_list

app_routes = Blueprint("app_routes", __name__)


def login_required(f):

    @wraps(f)
    def wrapper(*args, **kwargs):
        if 'user' in session:
            return f(*args, **kwargs)
        return "A logged-in user is required", 403
    return wrapper


def login_admin_required(f):

    @wraps(f)
    def wrapper(*args, **kwargs):
        from flask import current_app
        if 'user' in session and session['user'] in current_app.config["ADMIN_EMAILS"]:
            return f(*args, **kwargs)
        return "A logged-in admin is required", 403
    return wrapper


def is_user_admin():
    email = session["user"]
    return email in current_app.config["ADMIN_EMAILS"]


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
    hostname = current_app.config["PUBLIC_SERVER_NAME"]
    front_path = current_app.config["FRONTEND_CONFIRMED_PATHNAME"]
    return f"{protocol}{hostname}{front_path}?token={reservation.token}"


def get_login_link(token):
    from flask import current_app
    protocol = "http://" if current_app.config["DEBUG"] else "https://"
    hostname = current_app.config["PUBLIC_SERVER_NAME"]
    front_path = current_app.config["FRONTEND_LOGIN_PATHNAME"]
    return f"{protocol}{hostname}{front_path}?token={token}"


def get_mail_subject(text):
    return current_app.config["ORGANISM_FOR_EMAIL_SUBJECT"] + " " + text


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


@app_routes.route("/reservations", methods=["GET"])
@login_required
def get_reservations():
    page = request.args.get("page", 1, type=int)
    limit = request.args.get("limit", 10, type=int)

    event_id_arg = request.args.get("event_id", None)
    event_id = None
    if event_id_arg:
        try:
            event_id = int(event_id_arg)
        except TypeError:
            return "event_id query param should be an integer", 400

    email = session["user"]
    is_admin = is_user_admin()

    query = db.session.query(TReservations)

    if event_id:
        query = query.filter_by(id_event=event_id)
    if not is_admin:
        query = query.filter_by(email=email)
    query = query.paginate(page=page, per_page=limit)

    results = TReservationsSchema(many=True).dump(query.items)

    # reservations = query.all()
    return jsonify(
        {
            "page": page,
            "limit": limit,
            "total": query.total,
            "has_next": query.has_next,
            "has_prev": query.has_prev,
            "results": results,
        }
    )


@app_routes.route("/reservations", methods=["POST"])
def post_reservations():
    post_data = request.get_json()

    reservation = TReservationsSchema().load(post_data, session=db.session)

    # Récupération de l'événement cible, ce n'est pas un attribut de 'reservation' avant le commit.
    # TODO: return 404? Or just let the internal server error spread?
    event = GTEvents.query.filter_by(id=reservation.id_event).first()

    if not event.is_reservation_possible_for(reservation.nb_participants):
        return "", 422

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

    return TReservationsSchema().dumps(reservation)


@app_routes.route("/reservations/confirm", methods=["POST"])
def confirm_reservation():
    """Expects the reservation's token in the request body as JSON: {"resa_token": "12345abcde"}, if the corresponding
    reservation exists it is confirmed and a confirmation mail is sent."""
    token = request.get_json()["resa_token"]
    resa = db.first_or_404(db.select(TReservations).filter_by(token=token), description="Reservation not found")
    if resa.confirmed:
        return jsonify({"error": "Reservation already confirmed"}), 400

    event = resa.event
    if not event.is_reservation_possible_for(resa.nb_participants):
        return "", 422
    elif event.sum_participants + resa.nb_participants <= event.capacity:
        resa.liste_attente = False
    else:
        resa.liste_attente = True

    resa.confirmed = True

    db.session.add(resa)
    db.session.commit()

    if not resa.liste_attente:
        send_email(
            subject=get_mail_subject("Votre réservation est confirmée"),
            recipients=[resa.email],
            html=render_template(
                "resa_confirmed_mail.html",
                nb_places=resa.nb_participants,
                event=event.name
            )
        )
    else:
        send_email(
            subject=get_mail_subject("Votre réservation est en liste d'attente"),
            recipients=[resa.email],
            html=render_template(
                "confirmation_mail_on_liste_attente.html",
                nb_places=resa.nb_participants,
                event=event.name
            )
        )

    return "", 204


@app_routes.route("/reservations/<reservation_id>", methods=["PUT"])
@login_admin_required
def update_reservation(reservation_id):

    # Check : la réservation existe
    reservation = TReservations.query.get(reservation_id)
    if not reservation:
        return jsonify({"error": f"Reservation #{reservation_id} not found"}), 404

    post_data = request.get_json()
    validated_data = TReservationsUpdateSchema().load(post_data)
    for k, v in validated_data.items():
        setattr(reservation, k, v)
    db.session.add(reservation)
    db.session.commit()

    return TReservationsSchema().dumps(reservation), 200


@app_routes.route("/reservations/<reservation_id>", methods=["DELETE"])
@login_required
def cancel_reservation(reservation_id):
    is_admin = is_user_admin()

    # Check : la réservation existe
    reservation = TReservations.query.get(reservation_id)
    if not reservation:
        return jsonify({"error": f"Reservation #{reservation_id} not found"}), 404

    # Check : la réservation appartient à l'utilisateur OU is_admin
    user_email = session["user"]
    if not is_admin and reservation.email != user_email:
        return jsonify({"error": f"Reservation #{reservation_id} does not belong to {user_email}"}), 404

    if not reservation.confirmed:
        return jsonify({"error": f"Reservation #{reservation_id} is not confirmed and cannot be cancelled"}), 400

    if reservation.cancelled:
        return jsonify({"error": f"Reservation #{reservation_id} has already been cancelled"}), 400


    reservation.cancelled = True
    reservation.cancel_data = datetime.now()
    reservation.cancel_by = "admin" if is_admin else "utilisateur"
    db.session.add(reservation)
    db.session.commit()

    if not is_admin:
        # Envoi email confirmation d'annulation à l'utilisateur
        send_email(
            subject=get_mail_subject("Votre réservation a été annulée"),
            recipients=[reservation.email],
            html=render_template(
                "resa_cancelled_mail.html",
                reservation=reservation,
                event=reservation.event
            )
        )

        # Envoi notification aux administrateurs
        send_email(
            subject=get_mail_subject("Une réservation a été annulée"),
            recipients=[reservation.email],
            html=render_template(
                "admin_resa_cancelled_mail.html",
                reservation=reservation,
                event=reservation.event
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
    db.session.commit()

    send_email(
        "Lien de connexion sur site de réservation du PNG",
        recipients=[email],
        html=render_template(
            "login_mail.html",
            login_link=get_login_link(token.token)
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
    token = db.first_or_404(db.select(TTokens).filter_by(token=login_token),
                            description="The login token is invalid or expired")

    # Set a Session Cookie in the response.
    session['user'] = token.email
    from flask import current_app

    return jsonify({
        "is_admin": token.email in current_app.config["ADMIN_EMAILS"],
        "email": token.email
    }), 200


@app_routes.route("/export_reservation/<id>", methods=["GET"])
@login_admin_required
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
@login_admin_required
def post_bilans():
    post_data = request.get_json()
    bilan = TAnimationsBilansSchema().load(post_data, session=db.session)

    db.session.add(bilan)
    db.session.commit()
    db.session.close()
    return jsonify({"msg": "Données sauvegardées"})


@app_routes.route("/reservations/<id_reservation>", methods=["DELETE"])
@login_required
def delete_reservations(id_reservation):
    reservation = TReservations.query.get_or_404(id_reservation)
    db.session.delete(reservation)
    db.session.commit()
    return jsonify({"msg": "Données supprimées"})


@app_routes.route("/stats/global", methods=["GET"])
@login_admin_required
def get_stats_global():
    params = request.args
    data = query_stats_bilan(params)

    return jsonify(data)


@app_routes.route("/stats/charts/nb_day_before_resa", methods=["GET"])
@login_admin_required
def get_stats_nb_day_before_resa():
    params = request.args
    data = query_stats_animations_per_month(params)
    return jsonify(data)


@app_routes.route("/export/events")
@login_admin_required
def get_export_events():
    events = VExportBilan.query.all()
    results = VExportBilanSchema(many=True).dump(events)
    fields = VExportBilan.__table__.columns.keys()
    return to_csv_resp("export_bilan", results, fields, ";")
