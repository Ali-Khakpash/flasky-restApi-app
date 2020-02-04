from flask import Blueprint
from flask import request, make_response,jsonify 
from flask_sqlalchemy import SQLAlchemy
from Models.users import User,db,users_schema,user_schema
from flask_jwt_extended import create_access_token, jwt_required, get_raw_jwt, jwt_optional, get_jwt_identity, \
    get_jwt_claims
from db import jwt
from flask_login import login_user, current_user, login_required


user_routes = Blueprint("user_routes", __name__)



@jwt.user_claims_loader
def add_claims_to_access_token(user):
    return {'userr': user.password,
            'ass':'big'
            }

@jwt.user_identity_loader
def user_identity_lookup(user):
    return user.username



@user_routes.route('signup', methods=['POST'])
def create_user():
        data = request.get_json()
        data['password'] = User.generate_hash(data['password'])
        new_user = User(data['username'], data['password'])
        # new_author.updated = '2020-12-07 09:41:58'
        db.session.add(new_user)
        db.session.commit()
        return make_response(jsonify({"user": user_schema.dump(new_user)}))


@user_routes.route('signin', methods=['POST'])
def authenticate_user():
    data = request.get_json()
    user = User.query.filter_by(username=data['username']).first()
    if user is not None:
      if User.verify_hash(data['password'], user.password):
         login_user(user)
         access_token = create_access_token(identity =user)
         return make_response(jsonify({"access_token":access_token, "currentUser":current_user.username}))
    return make_response(jsonify({"error":"ops username or password is wrong"}))


# In a protected view, get the claims you added to the jwt with the
# get_jwt_claims() method
@user_routes.route('/protected', methods=['GET'])
@jwt_required
def protected():
    ret = {
        'current_identity': get_jwt_identity(),
        'current_roles': get_jwt_claims()['userr'],
        'a.s.s':get_jwt_claims()['ass']

    }
    return jsonify(ret), 200



@user_routes.route('', methods=['GET'])
def get_all_users():
    all_users =  User.query.all()
    return make_response(jsonify({"users": users_schema.dump(all_users)}))



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