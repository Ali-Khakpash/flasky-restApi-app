from astroid.bases import manager
from flask import Flask
from flask_jwt_extended import get_jwt_identity, get_current_user, verify_jwt_in_request
from flask_sqlalchemy import SQLAlchemy
from config import config
from routes.plans_routes import plans_routes
from routes.users_routes import user_routes
from Models.users import User
from Models.plans import Plan
from Models.terms import Terms
from Models.terms_taxonomy import Terms_Taxonomy
# from Models.authors import db,ma
# from Models.books import db,ma
from db import db,ma,jwt
# from routes.users_routes import jwt
from flask_authorize import Authorize
from login_handle import login_manager
from authorize import authorize
from services.email_verification.email import mail
from flask_migrate import Migrate

migrate = Migrate()


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
    mail.init_app(app)
    migrate.init_app(app,db)

    with app.app_context():
         db.create_all() #creats all table from model class
    app.register_blueprint(plans_routes, url_prefix='/api')
    app.register_blueprint(user_routes, url_prefix='/api')

    @login_manager.user_loader
    def load_user(curr_user):
        curr_user = get_jwt_identity()
        return User.query.filter_by(username=curr_user).first()

    return app
