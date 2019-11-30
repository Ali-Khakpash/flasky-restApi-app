from flask import Blueprint
from flask import request, make_response,jsonify 
from flask_sqlalchemy import SQLAlchemy
from Models.authors import Author,db,authors_schema

author_routes = Blueprint("author_routes", __name__)

#from Models.authors import Author
#from app import db

@author_routes.route('', methods=['POST'])
def create_author():
    # try:
    data = request.get_json()
    new_author = Author(data['first_name'], data['last_name'])
    #dummped = author_schema.dump(new_author)
    db.session.add(new_author)
    db.session.commit()
    return make_response('hghhghgh')

    # except Exception as e:
    #     print(e)
    #     #return response_with(resp.INVALID_INPUT_422)
    #     return make_response('mm')


@author_routes.route('get', methods=['GET'])
def get_all_author():
    all_authors =  Author.query.all()
    #return authors_schema.dump(all_authors)
    return make_response(jsonify({"authors": authors_schema.dump(all_authors)}))

    # except Exception as e:
    #     print(e)
    #     #return response_with(resp.INVALID_INPUT_422)
    #     return make_response('mm')



@author_routes.app_errorhandler(404)
def handle_404(err):
    return make_response('bad req')


@author_routes.app_errorhandler(400)
def handle_400(err):
    return make_response('bad request')