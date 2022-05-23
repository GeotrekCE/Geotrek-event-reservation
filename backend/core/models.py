import datetime
import json
from sqlalchemy import func, or_
from sqlalchemy.orm import aliased

from sqlalchemy.ext.hybrid import hybrid_property

from .env import db


from flask_sqlalchemy import BaseQuery

from pypnusershub.db.models import User

class GTEventsQuery(BaseQuery):

    def filter_properties(self, filters):
        if filters.get('search_name', None):
            search_name = filters.get('search_name', None)
            self = self.filter(GTEvents.name.ilike(f"%{search_name}%"))
            filters.pop("search_name")

        if "begin_date" in filters:
            self = self.filter(GTEvents.begin_date >= filters.pop("begin_date"))

        if "end_date" in filters:
            # set the end_date at 23h59 because a hour can be set in timestamp
            end_date = datetime.datetime.strptime(filters.pop("end_date"), "%Y-%m-%d")
            end_date = end_date.replace(hour=23, minute=59, second=59)
            self = self.filter(GTEvents.end_date <= end_date)

        if "bilan.annulation" in filters:
            canceled = json.loads(filters.pop("bilan.annulation"))
            tbilan = aliased(getattr(GTEvents, "bilan"))
            self = self.outerjoin(tbilan)
            if canceled:
                self = self.filter(
                    tbilan.annulation == True,
                )
            else:
                self = self.filter(
                    or_(
                        tbilan.annulation == None,
                        tbilan.annulation == False
                    )
                )

        # Généric filters
        for param in filters:
            if hasattr(GTEvents, param):
                self = self.filter(getattr(GTEvents, param) == filters.get(param))

        # Filter not deleted
        self = self.filter(GTEvents.deleted != True)

        return self


class GTEvents(db.Model):

    __tablename__ = "tourism_touristicevent"
    __table_args__ = {"schema": "public"}
    query_class = GTEventsQuery

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Unicode, nullable=False)
    description_teaser = db.Column(db.Unicode)
    participant_number = db.Column(db.Unicode)
    practical_info_fr = db.Column(db.Unicode)
    practical_info_en = db.Column(db.Unicode)
    begin_date = db.Column(db.Date)
    end_date = db.Column(db.Date)
    type_id = db.Column(db.Integer, db.ForeignKey("public.tourism_touristiceventtype.id"))
    published = db.Column(db.Boolean)
    deleted = db.Column(db.Boolean)

    reservations = db.relationship("TReservations", lazy="joined", backref=db.backref("event", lazy="joined"))

    bilan = db.relationship("TAnimationsBilans", lazy="joined", uselist=False)


    type = db.relationship("GTEventType", lazy="joined")

    @hybrid_property
    def sum_participants(self):
        return sum(r.sum_participants for r in self.reservations)

    @hybrid_property
    def sum_participants_liste_attente(self):
        return sum(r.sum_participants_liste_attente for r in self.reservations)

    @hybrid_property
    def massif(self):
        return db.session.query(func.animations.get_secteur_name(self.id)).first()[0]

    @massif.expression
    def massif(cls):
        return func.animations.get_secteur_name(cls.id)

class GTEventType(db.Model):

    __tablename__ = "tourism_touristiceventtype"
    __table_args__ = {"schema": "public"}
    id = db.Column(db.Integer, primary_key=True)
    pictogram = db.Column(db.Unicode, nullable=False)
    type = db.Column(db.Unicode, nullable=False)


class TReservations(db.Model):
    __tablename__ = "t_reservations"
    __table_args__ = {"schema": "animations"}
    id_reservation = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.Unicode, nullable=False)
    prenom = db.Column(db.Unicode)
    tel = db.Column(db.Unicode)
    commentaire = db.Column(db.Unicode)
    nb_adultes = db.Column(db.Integer, default=0)
    nb_moins_6_ans = db.Column(db.Integer, default=0)
    nb_6_8_ans = db.Column(db.Integer, default=0)
    nb_9_12_ans = db.Column(db.Integer, default=0)
    nb_plus_12_ans = db.Column(db.Integer, default=0)
    num_departement = db.Column(db.Unicode)
    id_numerisateur = db.Column(db.Integer, db.ForeignKey('utilisateurs.t_roles.id_role'))
    commentaire_numerisateur = db.Column(db.Unicode)
    liste_attente = db.Column(db.Boolean)
    id_event = db.Column(db.Integer, db.ForeignKey('public.tourism_touristicevent.id'))

    numerisateur = db.relationship("User", lazy="joined", uselist=False)

    @hybrid_property
    def sum_participants(self):
        if not self.liste_attente :
            return (self.nb_adultes  + self.nb_moins_6_ans + self.nb_6_8_ans + self.nb_9_12_ans + self.nb_plus_12_ans)
        return 0

    @hybrid_property
    def sum_participants_liste_attente(self):
        if self.liste_attente :
            return (self.nb_adultes  + self.nb_moins_6_ans + self.nb_6_8_ans + self.nb_9_12_ans + self.nb_plus_12_ans)
        return 0

    User

class TAnimationsBilans(db.Model):
    __tablename__ = "t_animations_bilans"
    __table_args__ = {"schema": "animations"}
    id_bilan = db.Column(db.Integer, primary_key=True)
    annulation = db.Column(db.Boolean)
    raison_annulation = db.Column(db.Unicode)
    nb_adultes = db.Column(db.Integer, default=0)
    nb_moins_6_ans = db.Column(db.Integer, default=0)
    nb_6_8_ans = db.Column(db.Integer, default=0)
    nb_9_12_ans = db.Column(db.Integer, default=0)
    nb_plus_12_ans = db.Column(db.Integer, default=0)
    id_numerisateur = db.Column(db.Integer)
    commentaire = db.Column(db.Unicode)
    id_event = db.Column(db.Integer, db.ForeignKey('public.tourism_touristicevent.id'))
