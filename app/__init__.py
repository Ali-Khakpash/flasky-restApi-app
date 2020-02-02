from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import config
from routes.plans_routes import plans_routes
from routes.users_routes import user_routes
from Models.users import User
from Models.plans import Plan
# from Models.authors import db,ma
# from Models.books import db,ma
from db import db,ma,jwt
# from routes.users_routes import jwt
from flask_authorize import Authorize
from login_handle import login_manager

authorize = Authorize()

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    app.config['JWT_BLACKLIST_ENABLED'] = True
    config[config_name].init_app(app)
    jwt.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)
    authorize.init_app(app)
    ma.init_app(app)
    with app.app_context():
         db.create_all() #creats all table from model class
    app.register_blueprint(plans_routes, url_prefix='/api')
    app.register_blueprint(user_routes, url_prefix='/api')

    @login_manager.user_loader
    def load_user(id):
        return User.query.filter_by(id=id).first()

    return app
    