from db import db,ma
from flask_login import UserMixin
from passlib.hash import pbkdf2_sha256 as sha256
from flask_sqlalchemy import SQLAlchemy
from marshmallow_sqlalchemy import ModelSchema
from marshmallow import fields
from Models.plans import Plan, plans_schema, paln_schema, PlanSchema
from login_handle import login_manager


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(120), unique = True,nullable = False)
    password = db.Column(db.String(120), nullable = False)
    plans = db.relationship('Plan', backref='user_plans', cascade="all, delete-orphan")


    def __init__(self, username, password, plans=[]):
        self.username = username
        self.password = password
        self.plans = plans

    @classmethod
    def find_by_username(cls, username):
        return cls.query.filter_by(username = username).first()
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
    username = fields.String(required=True)
    books = fields.Nested(PlanSchema, many=True, only=['username', 'desc', 'id'])

user_schema  = UserSchema(only=['id', 'username'])
users_schema = UserSchema(many=True)