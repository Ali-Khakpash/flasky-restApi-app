import os
import pickle
from flask import Blueprint, send_from_directory
from flask import redirect, request, make_response, jsonify, url_for, render_template_string
from flask import flash, redirect, render_template, current_app
import json
from flask_sqlalchemy import SQLAlchemy


from Models.users import User, db, users_schema, user_schema
from flask_jwt_extended import create_access_token, jwt_required, get_raw_jwt, jwt_optional, get_jwt_identity, \
    get_jwt_claims
from authorize import authorize
from db import jwt
from services.email_verification.token import generate_email_token, decode_token
from services.email_verification.email import send_email
from Models.roles import Role
from services.validator.signup import SignUp
from services.utils import list_to_string, dict_to_string, str_to_dict, allowed_file
from werkzeug.utils import secure_filename


user_routes = Blueprint("user_routes", __name__)



@user_routes.route('signup', methods=['POST'])
def create_user():
    data = request.get_json()
    validator = SignUp(data)
    if (validator.is_valid()):
        if (validator.check_password(data['password'])):
            if (validator.unique_fields(data)):
                data['password'] = User.generate_hash(data['password'])
                new_user = User(data['email'], data['password'])
                token = generate_email_token(data['email'])

                db.session.add(new_user)
                db.session.commit()

                url_conf = url_for('user_routes.verify_user', token=token, _external=True)
                html = render_template_string("<p> Welcome Thanks for Signing up. "
                                              "Please Follow The Below Link To Activate Your Account."
                                              "</p><br><p> <a href='{{url_conf}}'> {{url_conf}} </a> </p>",
                                              url_conf=url_conf)
                send_email(new_user.email, 'Email Verification', html)
                return make_response(jsonify(
                    {"message": "To complete your registration, please click the link we've sent to your email.",
                     "user": user_schema.dump(new_user), "tokend_email": token, 'url_for': url_conf})), 200

            return make_response(
                (jsonify({"errors": {"unique_fields": "user with this username or email exists"}}))), 422

        return make_response((jsonify({"errors": {
            "password_error": "password must contain at least 6 characters, one uppercase letter, and one letter"}}))), 422

    return make_response(jsonify({"errors": validator.iter_errors()})), 422


@user_routes.route('signin', methods=['POST'])
def authenticate_user():
    data = request.get_json()
    user = User.query.filter_by(email=data['email']).first()
    if (user):
        if User.verify_hash(data['password'], user.password) and user.isVerified:
            access_token = create_access_token(identity=user)
            return jsonify({"access_token": access_token, "status_code":200})

        elif (User.verify_hash(data['password'], user.password) and not user.isVerified):
            return make_response(jsonify({"error": "Please Verify Your Account"})), 422

    return make_response(jsonify({"error": "ops email or password is wrong"})), 401


@user_routes.route('verify', methods=['GET'])
def verify_user():
    email = decode_token(request.args.get('token'))
    user = User.query.filter_by(email=email).first()
    if (user):
        user.isVerified = True
        return redirect('http://127.0.0.1:5060/home?q=first_login', 302)
    return make_response('Ops Error')


@user_routes.route('edit_profile', methods=['PUT'])
@jwt_required
def edit_profile():
    data = request.get_json()
    user = User.query.filter_by(email=get_jwt_identity()).first()
    user.first_name = data['first_name']
    user.last_name = data['last_name']
    user.age = data['age']
    user.country = data['country']
    user.city = data['city']
    user.phone_number = data['phone_number']
    user.social_media_accounts = dict_to_string(data['social_media_accounts'])

    db.session.add(user)
    db.session.commit()

    new_dict = str_to_dict(user.social_media_accounts)

    return jsonify({'dfdf': new_dict['Skype'], 'status_code':200})



@user_routes.route('upload_avatar', methods=['PUT'])
@jwt_required
def upload_avatar():
        if 'file' not in request.files:
              return jsonify({'error':'No file part'}), 422
        file = request.files.get('file')
        if file.filename == '':
            return jsonify({'error':'No selected file'}), 422
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            user = User.query.filter_by(email=get_jwt_identity()).first()
            user.avatar_link = url_for('static', filename='uploads/images/'+filename, _external=True)
            db.session.add(user)
            db.session.commit()
            file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
            return jsonify({'res':file.content_type, 'status_code':200, 'avatar_url':url_for('static', filename='uploads/images/'+filename, _external=True)})
        else:
            return jsonify(res='please, upload just supported files')



@user_routes.route('home', methods=['GET'])
@jwt_required
def home():
    user_obj = User.query.filter_by(email=get_jwt_identity()).first()
    user_data = user_schema.dump(user_obj)
    return jsonify(user_data=user_data, status_code=200)
    





@user_routes.route('add_role', methods=['POST'])
@jwt_required
@authorize.has_role('SUPER_ADMIN')
def add_role():
    data = request.get_json()
    role_delete = Role(data['role_name'])
    role_delete.allowances = data['allowances']
    db.session.add(role_delete)
    db.session.commit()
    return make_response('Role Has Been Added')


@user_routes.route('assign_role', methods=['POST'])
@jwt_required
@authorize.has_role('SUPER_ADMIN')
def assign_role():
    data = request.get_json()
    user = User.query.filter_by(email=data['email']).first()
    role = Role.query.filter_by(name=data['role']).first()
    role.user_role.append(user)
    return make_response('Role Has Been Assigned')


# In a protected view, get the claims you added to the jwt with the
# get_jwt_claims() method
@user_routes.route('/protected', methods=['GET'])
@jwt_required
def protected():
    ret = {
        'current_identity': get_jwt_identity(),
        'current_roles': get_jwt_claims()['userr'],
        'a.s.s': get_jwt_claims()['ass']
    }

    return jsonify(ret), 200


@user_routes.route('', methods=['GET'])
def get_all_users():
    all_users = User.query.all()
    return make_response(jsonify({"users": users_schema.dump(all_users)}))


blacklist = set()


@jwt.token_in_blacklist_loader  # this might decrease the speed.to avoid,we can use redis,...
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



@user_routes.route('/protected2', methods=['GET'])
@jwt_required
def protected2():
    ret = {
        'current_identity': get_jwt_identity()
    }
    return jsonify(ret), 200


@jwt.user_identity_loader
def user_identity_lookup(user):
    return user.email