import datetime
import json

from flask import current_app
from sqlalchemy import func, or_, select, extract
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import aliased

from .env import db

from core.exceptions import (
    EventIsFull,
    UserEventNbExceded,
    NotBookable,
    ParticipantNbExceded,
)


class GTEventsQuery:
    def filter_properties(self, query, filters):
        if filters.get("search_name", None):
            search_name = filters.get("search_name", None)
            query = query.where(
                func.unaccent(GTEvents.name).ilike(func.unaccent(f"%{search_name}%"))
            )
            filters.pop("search_name")

        if "begin_date" in filters:
            query = query.where(GTEvents.begin_date >= filters.pop("begin_date"))

        if "end_date" in filters:
            # set the end_date at 23h59 because a hour can be set in timestamp
            end_date = datetime.datetime.strptime(
                filters.pop("end_date")[:10], "%Y-%m-%d"
            )
            end_date = end_date.replace(hour=23, minute=59, second=59)
            query = query.where(GTEvents.end_date <= end_date)

        if "bilan.annulation" in filters:
            canceled = json.loads(filters.pop("bilan.annulation"))
            tbilan = aliased(getattr(GTEvents, "bilan"))
            query = query.outerjoin(tbilan)
            if canceled:
                query = query.where(
                    tbilan.annulation == True,
                )
            else:
                query = query.where(
                    or_(tbilan.annulation == None, tbilan.annulation == False)
                )

        # Généric filters
        for param in filters:
            if hasattr(GTEvents, param) and filters.get(param):
                # Split multi choice
                if len(filters.get(param).split(",")) > 1:
                    query = query.where(
                        getattr(GTEvents, param).in_(filters.get(param).split(","))
                    )
                else:
                    query = query.where(getattr(GTEvents, param) == filters.get(param))

        # Filter not deleted
        query = query.where(GTEvents.deleted != True)
        return query


class GTEvents(db.Model):
    __tablename__ = "tourism_touristicevent"
    __table_args__ = {"schema": "public"}

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Unicode, nullable=False)
    description_teaser = db.Column(db.Unicode)
    bookable = db.Column(db.Boolean)
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
    cancelled = db.Column(db.Boolean)
    cancellation_reason_id = db.Column(
        db.Integer, db.ForeignKey("public.tourism_cancellationreason.id")
    )
    meeting_point = db.Column(db.Unicode)
    start_time = db.Column(db.Time)

    reservations = db.relationship(
        "TReservations", lazy="joined", backref=db.backref("event", lazy="joined")
    )
    bilan = db.relationship("TAnimationsBilans", lazy="joined", uselist=False)
    cancellation_reason = db.relationship(
        "GTCancellationReason", lazy="select", uselist=False
    )
    info = db.relationship("TEventInfo", lazy="joined", uselist=False)
    type = db.relationship("GTEventType", lazy="joined")

    @hybrid_property
    def sum_participants(self):
        return sum(
            r.sum_participants
            for r in self.reservations
            if r.confirmed and not r.cancelled
        )

    @hybrid_property
    def sum_participants_liste_attente(self):
        return sum(
            r.sum_participants_liste_attente
            for r in self.reservations
            if r.confirmed and not r.cancelled
        )

    @hybrid_property
    def sum_participants_adultes(self):
        return sum(
            r.nb_adultes
            for r in self.reservations
            if r.confirmed and not r.cancelled and not r.liste_attente
        )

    @hybrid_property
    def sum_participants_moins_6_ans(self):
        return sum(
            r.nb_moins_6_ans
            for r in self.reservations
            if r.confirmed and not r.cancelled and not r.liste_attente
        )

    @hybrid_property
    def sum_participants_6_8_ans(self):
        return sum(
            r.nb_6_8_ans
            for r in self.reservations
            if r.confirmed and not r.cancelled and not r.liste_attente
        )

    @hybrid_property
    def sum_participants_9_12_ans(self):
        return sum(
            r.nb_9_12_ans
            for r in self.reservations
            if r.confirmed and not r.cancelled and not r.liste_attente
        )

    @hybrid_property
    def sum_participants_plus_12_ans(self):
        return sum(
            r.nb_plus_12_ans
            for r in self.reservations
            if r.confirmed and not r.cancelled and not r.liste_attente
        )

    @hybrid_property
    def massif(self):
        return db.session.query(func.animations.get_secteur_name(self.id)).first()[0]

    @massif.expression
    def massif(cls):
        return func.animations.get_secteur_name(cls.id)

    def is_reservation_possible_for(self, nb_people, email):

        if not self.bookable:
            raise NotBookable

        # Test nombre de reservation par utilisateur
        # Selection animations par utilisateur
        from datetime import datetime

        query = select(func.count(TReservations.id_reservation)).where(
            TReservations.cancelled == False,
            TReservations.email == email,
            TReservations.confirmed == True,
            extract("year", TReservations.meta_create_date) == datetime.today().year,
        )
        nb_reservation = db.session.scalar(query)

        # On retranche un de façon a s'assurer que le nb d'animation
        # ne sera pas suppérieur une fois l'animation ajoutée
        if nb_reservation > current_app.config["NB_ANIM_MAX_PER_USER"] - 1:
            raise UserEventNbExceded

        if nb_people > current_app.config["NB_PARTICIPANTS_MAX_PER_ANIM_PER_USER"]:
            raise ParticipantNbExceded

        if not self.capacity:
            return True
        if self.sum_participants + nb_people <= self.capacity:
            return True
        if (
            self.sum_participants_liste_attente + nb_people
            <= current_app.config["LISTE_ATTENTE_CAPACITY"]
        ):
            return True
        raise EventIsFull


class GTCancellationReason(db.Model):
    __tablename__ = "tourism_cancellationreason"
    __table_args__ = {"schema": "public"}
    id = db.Column(db.Integer, primary_key=True)
    label = db.Column(db.Unicode, nullable=False)


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
    liste_attente = db.Column(db.Boolean, nullable=True)
    meta_create_date = db.Column(db.DateTime, default=datetime.datetime.now)
    meta_update_date = db.Column(
        db.DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now
    )
    token = db.Column(db.Unicode)
    confirmed = db.Column(db.Boolean, default=False)
    id_event = db.Column(
        db.Integer, db.ForeignKey("public.tourism_touristicevent.id"), nullable=False
    )
    cancelled = db.Column(db.Boolean, default=False)
    cancel_date = db.Column(db.DateTime, nullable=True)
    cancel_by = db.Column(db.Unicode, nullable=True)
    digitizer = db.Column(db.Unicode, nullable=True)

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
        if self.liste_attente is False:
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
        if self.liste_attente is True:
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


class TEventInfo(db.Model):
    __tablename__ = "t_event_info"
    __table_args__ = {"schema": "animations"}
    id_event_info = db.Column(db.Integer, primary_key=True)
    id_event = db.Column(db.Integer, db.ForeignKey("public.tourism_touristicevent.id"))
    info_rdv = db.Column(db.Unicode, default="")
    meta_create_date = db.Column(db.DateTime, default=datetime.datetime.now)
    meta_update_date = db.Column(
        db.DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now
    )


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
    used = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.datetime.now)
