from flask import Blueprint
from flask import request, make_response,jsonify 
from flask_sqlalchemy import SQLAlchemy
from Models.products import Product, db, products_schema, product_schema

product_routes = Blueprint("product_routes", __name__)


@product_routes.route('', methods=['POST'])
def create_author():
    data = request.get_json()
    new_product = Product(data['name'], data['desc'] , data['user_id'])
    db.session.add(new_product)
    db.session.commit()
    result = product_schema.dump(new_product)
    return make_response(jsonify({"product": result}))

@product_routes.route('', methods=['GET'])
def get_all_book():
    all_books =  Product.query.all()
    return make_response(jsonify({"products": products_schema.dump(all_books)}))


@product_routes.route('/<int:product_id>', methods=['GET'])
def get_book_detail(product_id):
    fetched = Product.query.get_or_404(product_id)
    product = product_schema.dump(fetched)
    return make_response(jsonify({"product": product}))


product_routes.route('/<int:product_id>', methods=['PUT'])
def update_book_detail(product_id):
    data = request.get_json()
    get_product = Product.query.get_or_404(product_id)
    get_product.name = data['name']
    get_product.desc = data['desc']
    db.session.add(get_product)
    db.session.commit()

    product = product_schema.dump(get_product)
    return make_response(jsonify({"book": product}))


@product_routes.route('/<int:product_id>', methods=['PATCH'])
def modify_book_detail(product_id):
    data = request.get_json()
    get_product = Product.query.get_or_404(product_id)
    if data.get('name'):
        get_product.name = data['name']
    if data.get('desc'):
        get_product.desc = data['desc']
    db.session.add(get_product)
    db.session.commit()
    product = product_schema.dump(get_product)
    return make_response(jsonify({"product": product}))


@product_routes.route('/<int:product_id>', methods=['DELETE'])
def delete_book(product_id):
    get_product= Product.query.get_or_404(product_id)
    db.session.delete(get_product)
    db.session.commit()

    return make_response('Deleted Successfully',204)




