from datetime import date, timedelta
from flask import render_template

from app import create_app
from core.models import GTEvents
from core.utils import send_email, get_mail_subject, stringify


def send_email_rappel_pour(event):
    recipients = [r.email for r in event.reservations if not r.cancelled and r.confirmed and not r.liste_attente]
    print(f"Envoi mail de rappel pour événement {event.name}. Destinataires : {recipients}")
    send_email(
        subject=get_mail_subject("C'est demain !"),
        recipients=recipients,
        html=render_template(
            "resa_confirmed_mail.html",
            event=stringify(event),
            event_info=stringify(event.info),
        )
    )


app = create_app()
with app.app_context():
    tomorrow = date.today() + timedelta(days=1)
    events = GTEvents.query.filter_by(begin_date=tomorrow)
    for event in events:
        send_email_rappel_pour(event)
