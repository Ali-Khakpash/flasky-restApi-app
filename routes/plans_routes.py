from flask import Blueprint
from flask import request, make_response,jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt_claims, verify_jwt_in_request
from flask_login import login_required, current_user
from flask_sqlalchemy import SQLAlchemy
from Models.plans import Plan, db, plans_schema, paln_schema
from authorize import authorize
from db import jwt
from functools import wraps

plans_routes = Blueprint("plans_routes", __name__)

@jwt.user_claims_loader
def add_claims_to_access_token(user):
    return {'current_user_id': user.id,
            'ass':'big'
            }
@jwt.user_identity_loader
def user_identity_lookup(user):
    return user.username

def admin_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()
        claims = get_jwt_claims()
        if claims['roles'] != 'admin':
            return jsonify(msg='Admins only!'), 403
        else:
            return fn(*args, **kwargs)
    return wrapper


@plans_routes.route('plans', methods=['POST'])
# @login_required
@jwt_required
def create_plan():
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


@plans_routes.route('plans', methods=['GET'])
def get_all_book():
    all_books =  Plan.query.all()
    return make_response(jsonify({"plans": plans_schema.dump(all_books)}))


@plans_routes.route('/<int:plan_id>', methods=['GET'])
def get_book_detail(plan_id):
    fetched = Plan.query.get_or_404(plan_id)
    plan = paln_schema.dump(fetched)
    return make_response(jsonify({"paln": plan}))


@plans_routes.route('plans/<int:plan_id>', methods=['PUT'])
@jwt_required
#@admin_required
def update_book_detail(plan_id):
     if(check_content_permission(plan_id) == False):
         return make_response(jsonify({"error": "unauthorized"}))
     data = request.get_json()
     plan_obj = check_content_permission(plan_id)
     plan_obj.title = data['title']
     plan_obj.short_desc= data['short_desc']
     db.session.add(plan_obj)
     db.session.commit()
     plan = paln_schema.dump(plan_obj)
     return make_response(jsonify({"plans": plan}))


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


@plans_routes.route('plans/<int:plan_id>', methods=['DELETE'])
@jwt_required
def delete_book(plan_id):
    if (check_content_permission(plan_id) == False):
        return make_response(jsonify({"error": "unauthorized"}))
    plan_obj = check_content_permission(plan_id)
    db.session.delete(plan_obj)
    db.session.commit()
    return make_response('Deleted Successfully',204)


def check_content_permission(id):
    plan_obj = Plan.query.get_or_404(id)
    if (plan_obj.owner_id == get_jwt_claims()['userr']):
        return plan_obj
    return False












