from email_validator import validate_email, EmailNotValidError, EmailSyntaxError
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

from marshmallow import fields, EXCLUDE, validates_schema, ValidationError, post_load

from core.models import (
    GTEvents,
    TReservations,
    TUsers,
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
    # numerisateur = fields.Nested(
    #     lambda: UserSchema(only=("identifiant", "id_role")), dump_only=True
    # )

    @post_load
    def validate_email(self, data, **kwargs):
        try:
            email_info = validate_email(data.email, check_deliverability=False)
        except EmailNotValidError as e:
            raise ValidationError(f"email is not valid: {e}")
        except EmailSyntaxError as e:
            raise ValidationError(f"email is not valid: {e}")
        data.email = email_info.normalized
        return data

    # @validates_schema
    # def validate_email(self, data, **kwargs):
    #     try:
    #         emailinfo = validate_email(data, check_deliverability=False)
    #
    #         # After this point, use only the normalized form of the email address,
    #         # especially before going to a database query.
    #         email = emailinfo.normalized
    #
    #     except EmailNotValidError as e:
    #
    #         # The exception message is human-readable explanation of why it's
    #         # not a valid (or deliverable) email address.
    #         print(str(e))
    #     if data["field_b"] >= data["field_a"]:
    #         raise ValidationError("field_a must be greater than field_b")


class TUsersSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = TUsers
        load_instance = True


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

    #reservations = fields.Nested(lambda: TReservationsSchema, many=True)
    type = fields.Nested(lambda: GTEventTypeSchema)
    bilan = fields.Nested(lambda: TAnimationsBilansSchema)
    sum_participants = fields.Integer(dump_only=True)
    sum_participants_liste_attente = fields.Integer(dump_only=True)
    massif = fields.Str(dump_only=True)
