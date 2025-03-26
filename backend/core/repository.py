from datetime import datetime

from sqlalchemy import func, select

from core.models import db, GTEvents, TAnimationsBilans


def query_stats_bilan(params):
    query = select(GTEvents).where(GTEvents.deleted != True)
    if "year" in params:
        query = query.where(
            func.date_part("year", GTEvents.begin_date) == params["year"]
        )

    # all filtered events
    events = db.session.scalars(query).unique().all()
    nb_events = len(events)

    # Animations avec réservation
    events_capacity = [e for e in events if e.capacity and e.capacity > 0]
    nb_events_capacity = len(events_capacity)
    sum_nb_participants = sum([d.sum_participants for d in events_capacity])
    sum_events_capacity = sum([d.capacity for d in events_capacity])

    # Taux de remplissage de toutes les animations
    taux_remplissage_global = (
        round(sum_nb_participants / sum_events_capacity, 3)
        if sum_events_capacity
        else 0
    )

    # Taux de remplissage moyen des animations
    taux_remplissage_moyen = (
        (
            sum([d.sum_participants / d.capacity for d in events_capacity])
            / nb_events_capacity
        )
        if nb_events_capacity > 0
        else 0
    )
    taux_remplissage_moyen = (
        round(taux_remplissage_moyen, 3) if taux_remplissage_moyen else 0
    )

    # Annulations
    query = select(func.count(GTEvents.id)).where(GTEvents.cancelled == True)
    if "year" in params:
        query = query.where(
            func.date_part("year", GTEvents.begin_date) == params["year"]
        )
    nb_annulation = db.session.scalar(query)

    # Animations passées
    events_passe = [
        e for e in events if (e.end_date or e.begin_date) < datetime.now().date()
    ]
    nb_events_passe = len(events_passe)

    # Animations passées avec réservation
    events_capacity_passe = [
        e
        for e in events_capacity
        if (e.end_date or e.begin_date) < datetime.now().date()
    ]
    nb_events_capacity_passe = len(events_capacity_passe)
    sum_nb_participants_passe = sum([d.sum_participants for d in events_capacity_passe])
    sum_events_capacity_passe = sum([d.capacity for d in events_capacity_passe])

    # Taux de remplissage de toutes les animations passées
    taux_remplissage_global_passe = (
        round(sum_nb_participants_passe / sum_events_capacity_passe, 3)
        if sum_events_capacity_passe
        else 0
    )

    # Taux de remplissage moyen des animations passées
    taux_remplissage_moyen_passe = (
        (
            sum([d.sum_participants / d.capacity for d in events_capacity_passe])
            / nb_events_capacity_passe
        )
        if nb_events_capacity_passe > 0
        else 0
    )
    taux_remplissage_moyen_passe = (
        round(taux_remplissage_moyen_passe, 3) if taux_remplissage_moyen_passe else 0
    )

    # Annulations passées
    query = select(func.count(GTEvents.id)).where(GTEvents.cancelled == True)
    if "year" in params:
        query = query.where(
            func.date_part("year", GTEvents.begin_date) == params["year"]
        )
        query = query.filter(GTEvents.begin_date < datetime.now())
    nb_annulation_passe = db.session.scalar(query)

    return {
        "nb_animations": nb_events,
        "nb_annulation": nb_annulation,
        "nb_animations_capacity": nb_events_capacity,
        "sum_animations_capacity": sum_events_capacity,
        "sum_nb_inscriptions": sum_nb_participants,
        "taux_remplissage_global": taux_remplissage_global,
        "taux_remplissage_moyen": taux_remplissage_moyen,
        "nb_animations_passe": nb_events_passe,
        "nb_annulation_passe": nb_annulation_passe,
        "nb_animations_capacity_passe": nb_events_capacity_passe,
        "sum_animations_capacity_passe": sum_events_capacity_passe,
        "sum_nb_inscriptions_passe": sum_nb_participants_passe,
        "taux_remplissage_global_passe": taux_remplissage_global_passe,
        "taux_remplissage_moyen_passe": taux_remplissage_moyen_passe,
    }
