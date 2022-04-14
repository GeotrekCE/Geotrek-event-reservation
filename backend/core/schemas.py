from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

from marshmallow import fields, EXCLUDE
from marshmallow_sqlalchemy.fields import Nested

from core.models import GTEvents, TReservations, GTEventType


class TReservationsSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = TReservations
        include_relationships = True
        load_instance = True
        unknown = EXCLUDE
    sum_participants = fields.Integer(dump_only=True)
    sum_participants_liste_attente  = fields.Integer(dump_only=True)


class GTEventTypeSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = GTEventType
        load_instance = True


class GTEventsSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = GTEvents
        include_relationships = True
        load_instance = True
    reservations = Nested(TReservationsSchema, many=True)
    type = Nested(GTEventTypeSchema)
    sum_participants = fields.Integer(dump_only=True)
    sum_participants_liste_attente  = fields.Integer(dump_only=True)
    massif = fields.Str(dump_only=True)