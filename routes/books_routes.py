from flask import Blueprint
from flask import request, make_response,jsonify 
from flask_sqlalchemy import SQLAlchemy
from Models.books import Book, db, books_schema, book_schema

book_routes = Blueprint("book_routes", __name__)


@book_routes.route('', methods=['POST'])
def create_author():
    data = request.get_json()
    new_book = Book(data['title'], data['year'] , data['author_id'])
    db.session.add(new_book)
    db.session.commit()
    result = book_schema.dump(new_book)
    return make_response(jsonify({"book": result}))

@book_routes.route('', methods=['GET'])
def get_all_book():
    all_books =  Book.query.all()
    return make_response(jsonify({"books": books_schema.dump(all_books)}))

