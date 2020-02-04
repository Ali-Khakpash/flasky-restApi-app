from flask import Blueprint
from flask import request, make_response,jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_login import login_required, current_user
from flask_sqlalchemy import SQLAlchemy
from Models.plans import Plan, db, plans_schema, paln_schema


plans_routes = Blueprint("plans_routes", __name__)


@plans_routes.route('plans', methods=['POST','GET'])
# @login_required
@jwt_required
def create_read_plan():
    if request.method == 'POST':
        data = request.get_json()
        curr_user = get_jwt_identity()
        new_plan = Plan(data['title'], data['short_desc'])
        new_plan.owner = current_user
        api_key = request.headers.get('Authorization')
        db.session.add(new_plan)
        db.session.commit()
        result = paln_schema.dump(new_plan)
        return make_response(jsonify({"plan": result , "header value":api_key,
                                      "current_user":[curr_user,"asshole"]
                                      }))


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




