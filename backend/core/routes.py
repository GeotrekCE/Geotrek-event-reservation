import pdb
from flask import Flask, jsonify, request, current_app, Blueprint
from core.models import db, GTEvents, TReservations
from core.schemas import GTEventsSchema, TReservationsSchema
from pypnusershub import routes as fnauth



app_routes = Blueprint('app_routes', __name__ )

@app_routes.route('/events')
@fnauth.check_auth(1)
def get_events():
    page = request.args.get('page', 1, type=int)
    limit = request.args.get('limit', 10, type=int)

    if "fields" in request.args:
        fields = request.args.getlist('fields', None)
        fields =  fields[0].split(',') + fields [1:]
    else:
        fields = None

    query_params = request.args.to_dict()

    # Clean query params
    for p in ("limit", "page", "fields") :
        if query_params.get(p, None):
            query_params.pop(p)


    # Ordonancement
    sort_col = "begin_date"
    if "sortBy" in request.args:
        sort_col = query_params.pop("sortBy")

    sort_order = "desc"
    try:
        sort_order_param = query_params.pop("sortDesc")
        if sort_order_param == "false":
            sort_order = "asc"
    except KeyError:
        sort_order = "desc"


    events = GTEvents.query.filter_properties(query_params)
    if hasattr(GTEvents, sort_col):
        model_sort_col = getattr(GTEvents, sort_col)
    else:
        model_sort_col = GTEvents.begin_date

    events = events.order_by(
        getattr(model_sort_col, sort_order)(),
        GTEvents.id.asc()
    )

    events = events.paginate(page=page, per_page=limit)

    results = GTEventsSchema(many=True, only=fields).dump(events.items)

    return jsonify({
        'page': page,
        'limit': limit,
        'total': events.total,
        'has_next': events.has_next,
        'has_prev': events.has_prev,
        'results': results
    })


@app_routes.route('/events/<id>')
@fnauth.check_auth(1)
def get_one_event(id):
    events = GTEvents.query.get_or_404(id)
    results = GTEventsSchema().dump(events)
    return jsonify(results)

@app_routes.route('/reservations', methods=['POST'])
@fnauth.check_auth(1)
def post_reservations():
    post_data = request.get_json()

    reservation = TReservationsSchema().load(post_data, session=db.session)

    db.session.add(reservation)
    db.session.commit()
    db.session.close()
    return jsonify({
        'msg': "OK"
    })


@app_routes.route('/reservations/<id_reservation>', methods=['DELETE'])
@fnauth.check_auth(1)
def delete_reservations(id_reservation):
    print(id_reservation)
    reservation = TReservations.query.get_or_404(id_reservation)
    db.session.delete(reservation)
    db.session.commit()
    return jsonify({
        'msg': "OK"
    })
