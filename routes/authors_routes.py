from flask import Blueprint
from flask import request, make_response,jsonify 
from flask_sqlalchemy import SQLAlchemy
from Models.authors import Author,db,authors_schema,author_schema
from flask_jwt_extended import jwt_required
from redis_db import redis_client

author_routes = Blueprint("author_routes", __name__)

#from Models.authors import Author
#from app import db

@author_routes.route('', methods=['POST'])
@jwt_required
def create_author():
    data = request.get_json()
    new_author = Author(data['first_name'], data['last_name'])
    # new_author.updated = '2020-12-07 09:41:58'
    db.session.add(new_author)
    db.session.commit()

    # user_id = str(redis_client.incrby('Author:Book:Number:ADay:'))
    # book_value = str(redis_client.incrby('number_of_article_aday'))
    # redis_client.hset('Author:Book:Number:ADay:' + user_id, 'number_of_article_aday', book_value)
    return make_response('hghhghgh')


@author_routes.route('', methods=['GET'])
def get_all_author():
    all_authors =  Author.query.all()
    return make_response(jsonify({"authors": authors_schema.dump(all_authors)}))


@author_routes.route('<int:author_id>', methods=['GET'])
def get_author_detail(author_id):
    fetched = Author.query.get(author_id)
    author = author_schema.dump(fetched) ##don't forget to remove the fucking (many=true)
    return make_response(jsonify({"authors": author}))


@author_routes.route('<int:author_id>', methods=['PUT'])
def update_author_detail(author_id):
    data = request.get_json()
    get_author = Author.query.get_or_404(author_id)
    get_author.first_name = data['first_name']
    get_author.last_name = data['last_name']
    import datetime
    get_author.updated = datetime.datetime.now()
    db.session.add(get_author)
    db.session.commit()
    author = author_schema.dump(get_author)
    return make_response(jsonify({"authors": author}))


@author_routes.route('<int:author_id>', methods=['PATCH'])
def modify_author_detail(author_id):
    data = request.get_json()
    get_author = Author.query.get(author_id)
    if data.get('first_name'):
       get_author.first_name = data['first_name']
    if data.get('last_name'):
       get_author.last_name = data['last_name'] 

    db.session.add(get_author)
    db.session.commit()

    author = author_schema.dump(get_author)
    return make_response(jsonify({"authors": author}))



@author_routes.route('<int:author_id>', methods=['DELETE'])
def delete_author(author_id):
    get_author = Author.query.get_or_404(author_id)
    db.session.delete(get_author)
    db.session.commit()

    return make_response('Deleted Successfully',204)



    



# @author_routes.app_errorhandler(404)
# def handle_404(err):
#     return make_response('bad req')


# @author_routes.app_errorhandler(400)
# def handle_400(err):
#     return make_response('bad request')