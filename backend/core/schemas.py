from email_validator import validate_email, EmailNotValidError, EmailSyntaxError
from marshmallow import fields, EXCLUDE, ValidationError, post_load, RAISE
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema, auto_field, SQLAlchemySchema

from core.models import (
    GTEvents,
    TReservations,
    GTEventType,
    TAnimationsBilans,
    VExportBilan,
    TEventInfo,
)


def validate_and_normalize_email(email):
    try:
        email_info = validate_email(email, check_deliverability=False)
    except EmailNotValidError as e:
        raise ValidationError(f"email is not valid: {e}")
    except EmailSyntaxError as e:
        raise ValidationError(f"email is not valid: {e}")
    return email_info.normalized


class VExportBilanSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = VExportBilan


class TReservationsSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = TReservations
        load_instance = True
        include_fk = True
        unknown = RAISE
        dump_only = (
            "id_reservation",
            "liste_attente",
            "confirmed",
            "meta_create_date",
            "meta_update_date",
            "event",
            "cancelled",
            "cancel_date",
            "cancel_by",
        )
        exclude = ("token",)

    event = fields.Nested("GTEventsSchema", only=("name", "begin_date"))
    sum_participants = fields.Integer(dump_only=True)
    sum_participants_liste_attente = fields.Integer(dump_only=True)

    @post_load
    def validate_and_normalize_email(self, data, **kwargs):
        data.email = validate_and_normalize_email(data.email)
        return data

    @post_load
    def set_zero_default_value_for_participants(self, data, **kwargs):
        NB_PARTICIPANTS_DEFAULT_VALUE = 0
        for prop in [
            "nb_adultes",
            "nb_moins_6_ans",
            "nb_6_8_ans",
            "nb_9_12_ans",
            "nb_plus_12_ans",
        ]:
            if getattr(data, prop) is None:
                setattr(data, prop, NB_PARTICIPANTS_DEFAULT_VALUE)
        return data


class TReservationsCreateByAdminSchema(TReservationsSchema):
    class Meta(TReservationsSchema.Meta):
        dump_only = (
            "id_reservation",
            "meta_create_date",
            "meta_update_date",
            "event",
            "cancelled",
            "cancel_date",
            "cancel_by",
        )

    confirmed = auto_field(load_default=True)
    liste_attente = fields.Boolean()


class TReservationsUpdateSchema(SQLAlchemySchema):
    class Meta:
        model = TReservations
        unknown = RAISE
        load_instance = False

    nom = auto_field(required=False)
    prenom = auto_field(required=False)
    tel = auto_field(required=False)
    email = auto_field(required=False)
    commentaire = auto_field()
    nb_adultes = auto_field()
    nb_moins_6_ans = auto_field()
    nb_6_8_ans = auto_field()
    nb_9_12_ans = auto_field()
    nb_plus_12_ans = auto_field()
    num_departement = auto_field()
    liste_attente = auto_field()
    confirmed = auto_field()

    @post_load
    def validate_and_normalize_email(self, data, **kwargs):
        try:
            data.email
        except AttributeError:
            return data
        data.email = validate_and_normalize_email(data.email)
        return data


class GTEventTypeSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = GTEventType
        load_instance = True


class TAnimationsBilansSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = TAnimationsBilans
        load_instance = True
        include_fk = True
        include_relationships = True


class TEventInfoSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = TEventInfo
        load_instance = False
        include_fk = True
        include_relationships = True
        dump_only = (
            "meta_create_date",
            "meta_update_date",
        )
        exclude = (
            "id_event",
            "id_event_info",
        )


class GTEventsSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = GTEvents
        include_relationships = True
        load_instance = True
        exclude = (
            "reservations",
            "info",
        )

    type = fields.Nested(lambda: GTEventTypeSchema)
    bilan = fields.Nested(lambda: TAnimationsBilansSchema)
    sum_participants = fields.Integer(dump_only=True)
    sum_participants_liste_attente = fields.Integer(dump_only=True)
    sum_participants_adultes = fields.Integer(dump_only=True)
    sum_participants_moins_6_ans = fields.Integer(dump_only=True)
    sum_participants_6_8_ans = fields.Integer(dump_only=True)
    sum_participants_9_12_ans = fields.Integer(dump_only=True)
    sum_participants_plus_12_ans = fields.Integer(dump_only=True)
    massif = fields.Str(dump_only=True)
