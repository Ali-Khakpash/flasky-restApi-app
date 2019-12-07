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


@book_routes.route('/<int:book_id>', methods=['GET'])
def get_book_detail(book_id):
    fetched = Book.query.get_or_404(book_id)
    book = book_schema.dump(fetched)
    return make_response(jsonify({"book": book}))


book_routes.route('/<int:book_id>', methods=['PUT'])
def update_book_detail(book_id):
    data = request.get_json()
    get_book = Book.query.get_or_404(book_id)
    get_book.title = data['title']
    get_book.year = data['year']
    db.session.add(get_book)
    db.session.commit()

    book = book_schema.dump(get_book)
    return make_response(jsonify({"book": book}))


@book_routes.route('/<int:book_id>', methods=['PATCH'])
def modify_book_detail(book_id):
    data = request.get_json()
    get_book = Book.query.get_or_404(book_id)
    if data.get('title'):
        get_book.title = data['title']
    if data.get('year'):
        get_book.year = data['year']
    db.session.add(get_book)
    db.session.commit()
    book = book_schema.dump(get_book)
    return make_response(jsonify({"book": book}))


@book_routes.route('/<int:id>', methods=['DELETE'])
def delete_book(book_id):
    get_book = Book.query.get_or_404(book_id)
    db.session.delete(get_book)
    db.session.commit()

    return make_response('Deleted Successfully',204)




