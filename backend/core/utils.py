import csv
import io
import logging

from flask import Response, current_app
from flask_mail import Message
from werkzeug.datastructures import Headers

logger = logging.getLogger(__name__)


def to_csv_resp(filename, data, columns, separator=";"):
    headers = Headers()
    headers.add("Content-Type", "text/plain")
    headers.add(
        "Content-Disposition", "attachment", filename="export_%s.csv" % filename
    )
    out = generate_csv_content(columns, data, separator)
    return Response(out, headers=headers)


def generate_csv_content(columns, data, separator):
    fp = io.StringIO()
    writer = csv.DictWriter(
        fp, columns, delimiter=separator, quoting=csv.QUOTE_ALL, extrasaction="ignore"
    )
    writer.writeheader()  # ligne d'entête

    for line in data:
        writer.writerow(line)
    fp.seek(0)  # Rembobinage du "fichier"
    return fp.read()  # Retourne une chaine


def transform_obj_to_flat_list(fields, data):
    flat_data = []
    for res in data:
        exp_res = {}
        for field in fields:
            tmp_res = res
            for i in field.split("."):
                tmp_res = tmp_res[i] if tmp_res else ""
            exp_res[field] = tmp_res
        flat_data.append(exp_res)
    return flat_data


def get_mail_subject(text):
    return current_app.config["ORGANISM_FOR_EMAIL_SUBJECT"] + " " + text


def send_email(subject, recipients, html):
    msg = Message(subject=subject, recipients=recipients, html=html)
    logger.info(f'Email envoyé "{subject}" à {recipients}')
    logger.debug(f"<<< EMAIL ENVOYÉ >>>\n{msg}\n<<< FIN EMAIL >>>\n")
    from app import mail

    mail.send(msg)


def _get_property_names(model_object):
    from sqlalchemy.ext.hybrid import hybrid_property

    if not model_object:
        return []
    return [
        p
        for p in dir(model_object)
        if not p.startswith("_")
        and (
            type(model_object.__class__.__dict__.get(p)) == property
            or type(model_object.__class__.__dict__.get(p)) == hybrid_property
        )
    ]


def _get_orm_attribute_names(model_object):
    if not model_object:
        return []
    return [a for a in model_object.__dict__.keys() if not a.startswith("_")]


def stringify(model_object):
    """Prend une instance de modèle et retourne un dict avec les attributs de l'ORM, les properties et les
    hybrid properties en clé. Les valeurs sont stringifiées :

    - None -> "--"
    - True -> "Oui"
    - False -> "None"
    """
    rv = {}

    def process(attributes):
        for a in attributes:
            v = getattr(model_object, a)
            if v is None:
                v = "--"
            elif v is True:
                v = "Oui"
            elif v is False:
                v = "Non"
            rv[a] = v

    process(_get_orm_attribute_names(model_object))
    process(_get_property_names(model_object))

    return rv
