from flask import Blueprint
from flask import request, make_response,jsonify
from flask_sqlalchemy import SQLAlchemy
from Models.plans import Plan, db, plans_schema, paln_schema


plans_routes = Blueprint("plans_routes", __name__)


@plans_routes.route('', methods=['POST'])
def create_author():
    data = request.get_json()
    new_plan = Plan(data['name'], data['desc'] , data['user_id'])
    db.session.add(new_plan)
    db.session.commit()
    result = paln_schema.dump(new_plan)
    return make_response(jsonify({"plan": result}))

@plans_routes.route('', methods=['GET'])
def get_all_book():
    all_books =  Plan.query.all()
    return make_response(jsonify({"plans": plans_schema.dump(all_books)}))


@plans_routes.route('/<int:plan_id>', methods=['GET'])
def get_book_detail(plan_id):
    fetched = Plan.query.get_or_404(plan_id)
    plan = paln_schema.dump(fetched)
    return make_response(jsonify({"paln": plan}))


plans_routes.route('/<int:plan_id>', methods=['PUT'])
def update_book_detail(plan_id):
    data = request.get_json()
    get_plan = Plan.query.get_or_404(plan_id)
    get_plan.name = data['name']
    get_plan.desc = data['desc']
    db.session.add(get_plan)
    db.session.commit()

    plan = paln_schema.dump(get_plan)
    return make_response(jsonify({"book": plan}))


@plans_routes.route('/<int:plan_id>', methods=['PATCH'])
def modify_book_detail(plan_id):
    data = request.get_json()
    get_plan = Plan.query.get_or_404(plan_id)
    if data.get('name'):
        get_plan.name = data['name']
    if data.get('desc'):
        get_plan.desc = data['desc']
    db.session.add(get_plan)
    db.session.commit()
    plan = paln_schema.dump(get_plan)
    return make_response(jsonify({"plan": plan}))


@plans_routes.route('/<int:plan_id>', methods=['DELETE'])
def delete_book(plan_id):
    get_plan= Plan.query.get_or_404(plan_id)
    db.session.delete(get_plan)
    db.session.commit()

    return make_response('Deleted Successfully',204)




