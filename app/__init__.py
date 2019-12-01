from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import config 
from routes.authors_routes import author_routes
from routes.books_routes import book_routes
from Models.authors import db,ma
from Models.books import db,ma


app = Flask(__name__)


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)
    db.init_app(app)
    ma.init_app(app)
    with app.app_context():
         db.create_all() #creats all table from model class 
    app.register_blueprint(author_routes, url_prefix='/api/authors')
    app.register_blueprint(book_routes, url_prefix='/api/books')

    
    # attach routes and custom error pages here
    return app
    