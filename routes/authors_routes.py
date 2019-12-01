from flask import Blueprint
from flask import request, make_response,jsonify 
from flask_sqlalchemy import SQLAlchemy
from Models.authors import Author,db,authors_schema,author_schema

author_routes = Blueprint("author_routes", __name__)

#from Models.authors import Author
#from app import db

@author_routes.route('', methods=['POST'])
def create_author():
    data = request.get_json()
    new_author = Author(data['first_name'], data['last_name'])
    db.session.add(new_author)
    db.session.commit()
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



# @author_routes.app_errorhandler(404)
# def handle_404(err):
#     return make_response('bad req')


# @author_routes.app_errorhandler(400)
# def handle_400(err):
#     return make_response('bad request')