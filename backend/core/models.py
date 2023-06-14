import datetime
import json

from flask_sqlalchemy import BaseQuery
from sqlalchemy import func, or_
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import aliased

from .env import db


# Le nombre maximale de personnes que l'on peut mettre en liste d'attente sur un événement.
LISTE_ATTENTE_CAPACITY = 10


class GTEventsQuery(BaseQuery):
    def filter_properties(self, filters):
        if filters.get("search_name", None):
            search_name = filters.get("search_name", None)
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
                    or_(tbilan.annulation == None, tbilan.annulation == False)
                )

        # Généric filters
        for param in filters:
            if hasattr(GTEvents, param) and filters.get(param):
                # Split multi choice
                if len(filters.get(param).split(",")) > 1:
                    self = self.filter(
                        getattr(GTEvents, param).in_(filters.get(param).split(","))
                    )
                else:
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
    capacity = db.Column(db.Integer)
    practical_info_fr = db.Column(db.Unicode)
    practical_info_en = db.Column(db.Unicode)
    target_audience = db.Column(db.Unicode)
    begin_date = db.Column(db.Date)
    end_date = db.Column(db.Date)
    type_id = db.Column(
        db.Integer, db.ForeignKey("public.tourism_touristiceventtype.id")
    )
    published = db.Column(db.Boolean)
    deleted = db.Column(db.Boolean)

    reservations = db.relationship(
        "TReservations", lazy="joined", backref=db.backref("event", lazy="joined")
    )

    bilan = db.relationship("TAnimationsBilans", lazy="joined", uselist=False)

    type = db.relationship("GTEventType", lazy="joined")

    @hybrid_property
    def sum_participants(self):
        return sum(r.sum_participants for r in self.reservations if r.confirmed)

    @hybrid_property
    def sum_participants_liste_attente(self):
        return sum(r.sum_participants_liste_attente for r in self.reservations if r.confirmed)

    @hybrid_property
    def massif(self):
        return db.session.query(func.animations.get_secteur_name(self.id)).first()[0]

    @massif.expression
    def massif(cls):
        return func.animations.get_secteur_name(cls.id)

    def is_reservation_possible_for(self, nb_people):
        if self.sum_participants + nb_people <= self.capacity:
            return True
        if self.sum_participants_liste_attente + nb_people <= LISTE_ATTENTE_CAPACITY:
            return True
        return False


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
    prenom = db.Column(db.Unicode, nullable=False)
    tel = db.Column(db.Unicode, nullable=False)
    email = db.Column(db.Unicode, nullable=False)
    commentaire = db.Column(db.Unicode)
    nb_adultes = db.Column(db.Integer, default=0)
    nb_moins_6_ans = db.Column(db.Integer, default=0)
    nb_6_8_ans = db.Column(db.Integer, default=0)
    nb_9_12_ans = db.Column(db.Integer, default=0)
    nb_plus_12_ans = db.Column(db.Integer, default=0)
    num_departement = db.Column(db.Unicode)
    liste_attente = db.Column(db.Boolean, default=True)
    meta_create_date = db.Column(db.DateTime)
    meta_update_date = db.Column(db.DateTime)
    token = db.Column(db.Unicode)
    confirmed = db.Column(db.Boolean)
    id_event = db.Column(db.Integer, db.ForeignKey("public.tourism_touristicevent.id"), nullable=False)
    cancelled = db.Column(db.Boolean, default=False)
    cancel_date = db.Column(db.DateTime, nullable=True)
    cancel_by = db.Column(db.Unicode, nullable=True)

    @property
    def nb_participants(self):
        return (
                self.nb_adultes
                + self.nb_moins_6_ans
                + self.nb_6_8_ans
                + self.nb_9_12_ans
                + self.nb_plus_12_ans
        )

    @hybrid_property
    def sum_participants(self):
        if not self.liste_attente:
            return (
                self.nb_adultes
                + self.nb_moins_6_ans
                + self.nb_6_8_ans
                + self.nb_9_12_ans
                + self.nb_plus_12_ans
            )
        return 0

    @hybrid_property
    def sum_participants_liste_attente(self):
        if self.liste_attente:
            return (
                self.nb_adultes
                + self.nb_moins_6_ans
                + self.nb_6_8_ans
                + self.nb_9_12_ans
                + self.nb_plus_12_ans
            )
        return 0

    # User


class TAnimationsBilans(db.Model):
    __tablename__ = "t_animations_bilans"
    __table_args__ = {"schema": "animations"}
    id_bilan = db.Column(db.Integer, primary_key=True)
    annulation = db.Column(db.Boolean, default=False)
    raison_annulation = db.Column(db.Unicode)
    nb_adultes = db.Column(db.Integer, default=0)
    nb_moins_6_ans = db.Column(db.Integer, default=0)
    nb_6_8_ans = db.Column(db.Integer, default=0)
    nb_9_12_ans = db.Column(db.Integer, default=0)
    nb_plus_12_ans = db.Column(db.Integer, default=0)
    id_numerisateur = db.Column(db.Integer)
    commentaire = db.Column(db.Unicode)
    meta_create_date = db.Column(db.DateTime)
    meta_update_date = db.Column(db.DateTime)
    id_event = db.Column(db.Integer, db.ForeignKey("public.tourism_touristicevent.id"))


class VExportBilan(db.Model):
    __tablename__ = "v_export_bilans_global"
    __table_args__ = {"schema": "animations"}
    id = db.Column(db.Integer, primary_key=True)
    zoning_city = db.Column(db.Unicode)
    zoning_district = db.Column(db.Unicode)
    name_fr = db.Column(db.Unicode)
    type = db.Column(db.Unicode)
    begin_date = db.Column(db.Date)
    end_date = db.Column(db.Date)
    capacity = db.Column(db.Integer)
    target_audience = db.Column(db.Unicode)
    resa_nb_total = db.Column(db.Integer)
    resa_nb_total_attente = db.Column(db.Integer)
    annulation = db.Column(db.Boolean)
    categorie_annulation = db.Column(db.Unicode)
    raison_annulation = db.Column(db.Unicode)
    bilan_nb_adultes = db.Column(db.Integer)
    bilan_nb_moins_6_ans = db.Column(db.Integer)
    bilan_nb_6_8_ans = db.Column(db.Integer)
    bilan_nb_9_12_ans = db.Column(db.Integer)
    bilan_nb_plus_12_ans = db.Column(db.Integer)
    bilan_commentaire = db.Column(db.Unicode)
    resa_nb_adultes = db.Column(db.Integer)
    resa_nb_moins_6_ans = db.Column(db.Integer)
    resa_nb_6_8_ans = db.Column(db.Integer)
    resa_nb_nb_9_12_ans = db.Column(db.Integer)
    resa_nb_plus_12_ans = db.Column(db.Integer)
    resa_nb_adultes_attente = db.Column(db.Integer)
    resa_nb_moins_6_ans_attente = db.Column(db.Integer)
    resa_nb_6_8_ans_attente = db.Column(db.Integer)
    resa_nb_9_12_ans_attente = db.Column(db.Integer)
    resa_nb_plus_12_ans_attente = db.Column(db.Integer)
    published = db.Column(db.Boolean)


class TTokens(db.Model):
    __tablename__ = "t_tokens"
    __table_args__ = {"schema": "animations"}
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.Unicode, nullable=False)
    token = db.Column(db.Unicode, nullable=False)
    used = db.Column(db.Boolean)
    created_at = db.Column(db.DateTime)
