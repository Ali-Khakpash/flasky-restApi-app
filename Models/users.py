from db import db,ma
from passlib.hash import pbkdf2_sha256 as sha256
from flask_sqlalchemy import SQLAlchemy
from marshmallow_sqlalchemy import ModelSchema
from marshmallow import fields
from Models.products import ProductSchema


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(120), unique = True,nullable = False)
    password = db.Column(db.String(120), nullable = False)
    products = db.relationship('Product', backref='user_products', cascade="all, delete-orphan")


    def __init__(self, username, password, products=[]):
        self.username = username
        self.password = password
        self.products = products

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
    books = fields.Nested(ProductSchema, many=True, only=['name', 'desc', 'id'])

user_schema  = UserSchema()
users_schema = UserSchema(many=True)