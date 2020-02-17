from flask import Blueprint
from flask import request, make_response,jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt_claims, verify_jwt_in_request
from flask_login import login_required, current_user
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
from sqlalchemy.sql import label

from Models.plans import Plan, db, plans_schema, paln_schema
from Models.terms import Terms, terms_schema
from Models.terms_taxonomy import Terms_Taxonomy
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
    #filter_by
    #all_books =  Plan.query.filter_by(title = 'mountaining',short_desc = 'amazing')

    #order_by
    #all_books = Plan.query.order_by(Plan.time_created.desc())
    # all_books = Plan.query.order_by(Plan.time_created.desc())

    # group_by
    #all_books = db.session.query(Plan.short_desc.label('short_desc'),func.count(Plan.id).label('number')).group_by(Plan.short_desc).all()
    #all_books = db.session.query(func.count(Plan.id),Plan.title).group_by(Plan.title).all()

    #having
    #all_books = db.session.query(Plan.title, func.count(Plan.id)).group_by(Plan.title).having(func.count(Plan.id) ==1).all()

    # label
    all_books = db.session.query(Plan.short_desc, func.count(Plan.id).label('number')).group_by(Plan.short_desc).all()

    all_books = plans_schema.dump(all_books)


    return make_response(jsonify({"plans": all_books}))


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


@plans_routes.route('plans/category', methods=['POST','GET'])
def create_catogory():
    if request.method == 'POST':
        data = request.get_json()
        term = Terms(data['category'])
        db.session.add(term)
        db.session.commit()

        term_taxonomy = Terms_Taxonomy(term.term_id, 'tag')
        db.session.add(term_taxonomy)
        db.session.commit()

    #term_list = Terms.query.all()
    # return make_response(jsonify({"term_list": terms_schema.dump(term_list)}))
    term_list = Terms.query.all()
    category_list = db.session.query(Terms,Terms_Taxonomy).filter(Terms.term_id == Terms_Taxonomy.term_id).all()
    return make_response(repr(type(category_list)))








def check_content_permission(id):
    plan_obj = Plan.query.get_or_404(id)
    if (plan_obj.owner_id == get_jwt_claims()['userr']):
        return plan_obj
    return False












