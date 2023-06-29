from datetime import datetime

from sqlalchemy import func

from core.models import db, GTEvents, TAnimationsBilans


def query_stats_animations_per_month(params):
    query = (
        db.session.query(
            func.date_part("YEAR", GTEvents.begin_date),
            func.date_part("MONTH", GTEvents.begin_date),
            func.count(GTEvents.id),
        )
        .filter(GTEvents.deleted != True)
        .group_by(
            func.date_part("YEAR", GTEvents.begin_date),
            func.date_part("MONTH", GTEvents.begin_date),
        )
        .order_by(
            func.date_part("YEAR", GTEvents.begin_date),
            func.date_part("MONTH", GTEvents.begin_date),
        )
    )
    data = query.all()

    annees = []
    results = {}
    for d in data:
        annee = int(d[0])
        if not annee in annees:
            annees.append(annee)
        results[annee] = results[annee] if d[0] in results else []
        results[d[0]].append((d[1], d[2]))

    formated_results = []
    for annee in annees:
        formated_results.append({"name": annee, "data": results[annee]})
    return formated_results


def query_stats_bilan(params):
    query = GTEvents.query.filter(GTEvents.deleted != True)
    if "year" in params:
        query = query.filter(
            func.date_part("year", GTEvents.begin_date) == params["year"]
        )
    nb_events = query.count()
    events = query.all()

    # events with capacity
    events_capacity = [e for e in events if e.capacity and e.capacity > 0]
    sum_nb_participant = sum([d.sum_participants for d in events_capacity])
    sum_clean_nb_participants = sum([d.capacity for d in events_capacity])
    # Taux de remplissage de toutes les animations
    taux_remplissage = (
        sum([d.sum_participants / d.capacity for d in events_capacity]) / nb_events
    )

    # Taux de remplissage des animations passées
    taux_remplissage_passe = (
        sum(
            [
                d.sum_participants / d.capacity
                for d in events_capacity
                if (
                    (d.end_date or datetime.now().date())
                    < datetime.now().date()
                    # and not getattr(d, "bilan", {}).annulation
                )
            ]
        )
        / nb_events
    )

    query = db.session.query(func.count(GTEvents.id)).filter(GTEvents.cancelled == True)
    if "year" in params:
        query = query.filter(
            func.date_part("year", GTEvents.begin_date) == params["year"]
        )
    nb_annulation = query.scalar()

    return {
        "nb_animations": nb_events,
        "nb_annulation": nb_annulation,
        "sum_nb_inscriptions": sum_nb_participant,
        "sum_nb_participants_possible": sum_clean_nb_participants,
        "taux_remplissage": taux_remplissage,
        "taux_remplissage_passe": taux_remplissage_passe,
    }
