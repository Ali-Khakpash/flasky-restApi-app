from db import db,ma
from flask_sqlalchemy import SQLAlchemy
from marshmallow_sqlalchemy import ModelSchema
from marshmallow import fields
#from app import db


class Product(db.Model):
    __tablename__ = 'products'
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    name = db.Column(db.String(50))
    desc = db.Column(db.String(200))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __init__(self, name, desc, user_id=None):
        self.name = name
        self.desc = desc
        self.user_id = user_id

# class ProductSchema(ma.Schema):
#     class Meta:
#         # Fields to expose
#         fields = ("id","title", "year","author_id")
# product_schema = ProductSchema()
# products_schema = ProductSchema(many=True)

class ProductSchema(ModelSchema):
    class Meta(ModelSchema.Meta):
        model = Product
        sqla_session = db.session
    id = fields.Number(dump_only=True)
    name = fields.String(required=True)
    desc = fields.String(required=True)
    user_id = fields.Integer()

product_schema = ProductSchema()
products_schema = ProductSchema(many=True)