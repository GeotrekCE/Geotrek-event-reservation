from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

from marshmallow import fields, EXCLUDE

from core.models import (
    GTEvents,
    TReservations,
    GTEventType,
    TAnimationsBilans,
    VExportBilan,
)

# from pypnusershub.db.models import User


class VExportBilanSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = VExportBilan


# class UserSchema(SQLAlchemyAutoSchema):
#     class Meta:
#         model = User
#         load_instance = True


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

    reservations = fields.Nested(lambda: TReservationsSchema, many=True)
    type = fields.Nested(lambda: GTEventTypeSchema)
    bilan = fields.Nested(lambda: TAnimationsBilansSchema)
    sum_participants = fields.Integer(dump_only=True)
    sum_participants_liste_attente = fields.Integer(dump_only=True)
    massif = fields.Str(dump_only=True)
