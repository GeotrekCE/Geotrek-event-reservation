from flask import url_for

import json
from sqlalchemy import select

from core.models import TTokens
from core.env import db

from .fixtures import (
    ADMIN_EMAIL,
    headers,
)


def login(client, user_mail=None):
    if not user_mail:
        user_mail = ADMIN_EMAIL

    data = {"email": user_mail}

    client.post(
        url_for("app_routes.send_login_email"), data=json.dumps(data), headers=headers
    )
    # Get token manually
    token = db.session.scalars(
        select(TTokens)
        .where(TTokens.used == False, TTokens.email == user_mail)
        .order_by(TTokens.created_at.desc())
    ).first()
    client.post(
        url_for("app_routes.login"),
        data=json.dumps({"login_token": token.token}),
        headers=headers,
    )
