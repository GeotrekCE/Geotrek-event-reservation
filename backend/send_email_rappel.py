from datetime import date, timedelta
import logging

from flask import render_template

from app import create_app
from core.models import GTEvents
from core.utils import send_email, get_mail_subject, stringify

logger = logging.getLogger(__name__)


def send_email_rappel_pour(event):
    recipients = [
        r.email
        for r in event.reservations
        if not r.cancelled and r.confirmed and not r.liste_attente
    ]
    logger.info(
        f"Envoi mail de rappel pour événement {event.name}. Destinataires : {recipients}"
    )
    for recipient in recipients:
        send_email(
            subject=get_mail_subject(f"{event.name}, c'est demain !"),
            recipients=[recipient],
            html=render_template(
                "rappel_event.html",
                event=stringify(event),
                event_info=stringify(event.info),
            ),
        )


if __name__ == "__main__":
    app = create_app()
    with app.app_context():
        tomorrow = date.today() + timedelta(days=1)
        logger.info(
            f"Envoi du mail de rappel pour les événements ayant lieu le {tomorrow}"
        )
        events = GTEvents.query.filter_by(begin_date=tomorrow)
        for event in events:
            send_email_rappel_pour(event)
        logger.info(f"Mail de rappel envoyé pour {events.count()} événement(s).")
