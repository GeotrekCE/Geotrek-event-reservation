from email_validator import validate_email, EmailNotValidError, EmailSyntaxError
from marshmallow import fields, EXCLUDE, ValidationError, post_load
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

from core.models import (
    GTEvents,
    TReservations,
    GTEventType,
    TAnimationsBilans,
    VExportBilan,
)


class VExportBilanSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = VExportBilan


class TReservationsSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = TReservations
        include_relationships = True
        load_instance = True
        include_fk = True
        unknown = EXCLUDE

    sum_participants = fields.Integer(dump_only=True)
    sum_participants_liste_attente = fields.Integer(dump_only=True)

    @post_load
    def validate_and_normalize_email(self, data, **kwargs):
        try:
            email_info = validate_email(data.email, check_deliverability=False)
        except EmailNotValidError as e:
            raise ValidationError(f"email is not valid: {e}")
        except EmailSyntaxError as e:
            raise ValidationError(f"email is not valid: {e}")
        data.email = email_info.normalized
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


class GTEventsSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = GTEvents
        include_relationships = True
        load_instance = True

    type = fields.Nested(lambda: GTEventTypeSchema)
    bilan = fields.Nested(lambda: TAnimationsBilansSchema)
    sum_participants = fields.Integer(dump_only=True)
    sum_participants_liste_attente = fields.Integer(dump_only=True)
    massif = fields.Str(dump_only=True)
