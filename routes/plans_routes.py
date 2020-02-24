from pprint import pprint

from flask import Blueprint
from flask import request, make_response,jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt_claims, verify_jwt_in_request
from flask_login import login_required, current_user
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func, select, join
from sqlalchemy.orm import aliased
from sqlalchemy.sql import label

from Models.plans import Plan, db, plans_schema, paln_schema
from Models.terms import Terms, terms_schema
from Models.terms_taxonomy import Terms_Taxonomy, terms_taxonomy_schema,term_taxonomy_schema
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

        # category_oject = db.session.query(Terms).\
        #     filter_by(name=data['category']).\
        #     join(Terms.terms_taxonomies).\
        #     filter(Terms_Taxonomy.taxonomy == 'category')
        # category = terms_schema.dump(category_oject)

        length = len(data['category'])
        for i in range(length):
            category_oject = Terms.query.filter_by(name=data['category'][i]). \
                join(Terms.terms_taxonomies). \
                filter(Terms_Taxonomy.taxonomy == 'category').first()

            term_taxo = Terms_Taxonomy.query.get(category_oject.term_id)
            term_taxo.term_taxonomy_plan.append(new_plan)

        db.session.add(new_plan)
        db.session.commit()
        result = paln_schema.dump(new_plan)
        return make_response(jsonify({"plan": result ,
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
        term = Terms(data['name'])

        query_check = db.session.query(Terms).\
            filter_by(name=data['name']).\
            join(Terms.terms_taxonomies).\
            filter(Terms_Taxonomy.taxonomy == 'category')

        if len( terms_schema.dump(query_check))==0 :
            #return make_response(jsonify({"term_list": len( terms_schema.dump(query_check))}))
            db.session.add(term)
            db.session.commit()

            term_taxonomy = Terms_Taxonomy(term.term_id, 'category')
            db.session.add(term_taxonomy)
            db.session.commit()


    # term_list = Terms.query.all()
    # return make_response(jsonify({"term_list": terms_schema.dump(term_list)}))

    a_alias = aliased(Terms_Taxonomy)
    category_list = db.session.query(Terms).\
        join(Terms.terms_taxonomies).\
        join(a_alias, Terms.terms_taxonomies).\
        filter(Terms_Taxonomy.taxonomy=='category')
    return make_response(jsonify({"term_list": terms_schema.dump(category_list)}))

    # term_taxo_q = select([Terms_Taxonomy.parent]).\
    #     alias()
    # category_list = db.session.query(Terms). \
    #     join(term_taxo_q, term_taxo_q.term_id==Terms.term_id)
    # return make_response(jsonify({"term_list": terms_schema.dump(category_list)}))


@plans_routes.route('plans/plans_of_category', methods=['POST'])
def list_plans_of_category():
    data = request.get_json()
    category_oject = db.session.query(Terms). \
        filter_by(name=data['category']). \
        join(Terms.terms_taxonomies). \
        filter(Terms_Taxonomy.taxonomy == 'category').first()

    category_id = Terms_Taxonomy.query.get(category_oject.term_id).term_taxonomy_id
    # two below queries work
    plansofcategory = Plan.query.join(Terms_Taxonomy.term_taxonomy_plan).filter(Terms_Taxonomy.term_id == category_id).all()
    plansofcategory = db.session.query(Plan).\
        join(Terms_Taxonomy.term_taxonomy_plan).\
        filter(Terms_Taxonomy.term_id == category_id)


    #Pagination
    paginated_obj = plansofcategory.paginate(1, 1, False).items
    return make_response(jsonify({"plans_of_category": plans_schema.dump(paginated_obj)}))


    #return make_response(jsonify({"plans_of_category": TermsTaxonomySchema.dump(term_taxo)}))
    #return make_response(jsonify({"plans_of_category": category_oject.term_id}))
    #return make_response(jsonify({"plans_of_category": category_id}))





def check_content_permission(id):
    plan_obj = Plan.query.get_or_404(id)
    if (plan_obj.owner_id == get_jwt_claims()['userr']):
        return plan_obj
    return False












