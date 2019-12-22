from flask import Blueprint
from flask import request, make_response,jsonify 
from flask_sqlalchemy import SQLAlchemy
from Models.books import Book, db, books_schema, book_schema
from redis_db import redis_client

book_routes = Blueprint("book_routes", __name__)


@book_routes.route('', methods=['POST'])
def create_author():
    data = request.get_json()
    new_book = Book(data['title'], data['year'] , data['author_id'])

    # book_value = str(redis_client.hincrby('Author:' + data['author_id'], 'number_of_article_aday', amount=1))#redis hsah to check number of books posted by an author
    # redis_client.hset('Author:' + data['author_id'], 'number_of_article_aday', book_value)

    if(redis_client.hexists('Author:' + data['author_id'], 'number_of_article_aday')):
      author_hash = redis_client.hgetall('Author:' + data['author_id'])

      if(author_hash['number_of_article_aday'] <= str(2)):
          db.session.add(new_book)
          db.session.commit()
          book_value = str(redis_client.hincrby('Author:' + data['author_id'], 'number_of_article_aday',amount=1))  # redis hsah to check number of books posted by an author
          redis_client.hset('Author:' + data['author_id'], 'number_of_article_aday', book_value)
    else:
          db.session.add(new_book)
          db.session.commit()
          book_value = str(redis_client.hincrby('Author:' + data['author_id'], 'number_of_article_aday',amount=1))  # redis hsah to check number of books posted by an author
          redis_client.hset('Author:' + data['author_id'], 'number_of_article_aday', book_value)


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




