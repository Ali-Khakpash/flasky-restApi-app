from flask import Blueprint
from flask import request, make_response,jsonify 
from flask_sqlalchemy import SQLAlchemy
from Models.users import User,db,users_schema,user_schema
from flask_jwt_extended import create_access_token,jwt_required,get_raw_jwt
from db import jwt
from redis_db import redis_client
from rbac_fl import rbac
from Models.role import Role


user_routes = Blueprint("user_routes", __name__)


@user_routes.route('', methods=['POST'])
# @rbac.allow(['anonmous'], methods=['POST'])
def create_user():
        data = request.get_json()
        data['password'] = User.generate_hash(data['password'])
        new_user = User(data['username'], data['password'])
        # new_author.updated = '2020-12-07 09:41:58'
        # r = Role('user')
        # new_user.add_role(r)
        admin_role = Role.query.filter_by(name='admin').first()
        admin_role.users.append(new_user)
        db.session.add(new_user)
        db.session.commit()
        return make_response(jsonify({"user": user_schema.dump(new_user)}))



@user_routes.route('login', methods=['POST'])
def authenticate_user():
    data = request.get_json()
    current_user = User.find_by_username(data['username'])

    if User.verify_hash(data['password'], current_user.password):
       access_token = create_access_token(identity =data['username'])
       # resp = {
       #     "access_token": create_access_token(identity =data['username']),
       #     "user_id": current_user.id
       # }

       #user_id = str(redis_client.incrby('Author:Book:Number:ADay:'))
       #book_value = str(redis_client.incrby('number_of_article_aday'))
       #redis_client.hset('Author:' + data['username'], 'number_of_article_aday', '0')
       rbac.set_user_loader(current_user)

       return make_response(jsonify({"User": access_token}))



blacklist = set()

@jwt.token_in_blacklist_loader #this might decrease the speed.to avoid,we can use redis,...
def check_if_token_in_blacklist(decrypted_token):
    jti = decrypted_token['jti']
    return jti in blacklist

# Endpoint for revoking the current users access token
@user_routes.route('logout', methods=['DELETE'])
@jwt_required
def logout():
    jti = get_raw_jwt()['jti']
    blacklist.add(jti)
    return jsonify({"msg": "Successfully logged out"}), 200