from flask import current_app
from flask_migrate import Migrate

from db import db, ma
from flask_login import UserMixin
from passlib.hash import pbkdf2_sha256 as sha256
from flask_sqlalchemy import SQLAlchemy
from marshmallow_sqlalchemy import ModelSchema
from marshmallow import fields
from Models.groups import Group
from flask_authorize import RestrictionsMixin, AllowancesMixin
from flask_authorize import PermissionsMixin
from Models.roles import Role

UserGroup = db.Table(
    'user_group', db.Model.metadata,
    db.Column('user_id', db.Integer, db.ForeignKey('users.id')),
    db.Column('group_id', db.Integer, db.ForeignKey('groups.id'))
)

UserRole = db.Table(
    'user_role', db.Model.metadata,
    db.Column('user_id', db.Integer, db.ForeignKey('users.id')),
    db.Column('role_id', db.Integer, db.ForeignKey('roles.id'))
)


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    password = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=False, nullable=False)
    isVerified = db.Column(db.Boolean, nullable=False, default=False)
    full_name = db.Column(db.String(120), unique=False, nullable=True)
    age = db.Column(db.Integer, unique=False, nullable=True)
    location = db.Column(db.String(120), unique=False, nullable=True)
    phone_number = db.Column(db.String(120), unique=False, nullable=True)
    social_media_accounts = db.Column(db.String(120), unique=False, nullable=True)
    avatar_link = db.Column(db.String(120), nullable=True)
    roles = db.relationship('Role', secondary=UserRole, backref=db.backref('user_role', lazy='dynamic'))
    groups = db.relationship('Group', secondary=UserGroup)

    def __init__(self, email, password):
        self.email = email
        self.password = password

    @classmethod
    def find_by_username(cls, username):
        return cls.query.filter_by(username=username).first()

    @staticmethod
    def generate_hash(password):
        return sha256.hash(password)

    @staticmethod
    def verify_hash(password, hash):
        return sha256.verify(password, hash)


class UserSchema(ModelSchema):
    class Meta(ModelSchema.Meta):
        model = User
        sqla_session = db.session

    id = fields.Number(dump_only=True)
    email = fields.String(required=True)
    full_name = fields.String(dump_only=True)
    age = fields.Integer(dump_only=True)
    location = fields.String(dump_only=True)
    phone_number = fields.String(dump_only=True)
    social_media_accounts = fields.String(dump_only=True)
    avatar_link = fields.String(dump_only=True)

    # books = fields.Nested(PlanSchema, many=True, only=['username', 'desc', 'id'])


user_schema = UserSchema(only=['id', 'email', 'full_name', 'location', 'phone_number', 'social_media_accounts', 'avatar_link', 'age'])
users_schema = UserSchema(many=True)
