from flask_sqlalchemy import SQLAlchemy
from db import db,ma
#from app import db

class Author(db.Model):
    __tablename__ = 'authors'
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    first_name = db.Column(db.String(20))
    last_name = db.Column(db.String(20))
    created = db.Column(db.DateTime, server_default=db.func.now())
    books = db.relationship('Book', backref='Author',cascade="all, delete-orphan")

    def __init__(self, first_name, last_name):
        self.first_name = first_name
        self.last_name = last_name

class AuthorSchema(ma.Schema):
    class Meta:
        # Fields to expose
        fields = ("id","first_name", "last_name", "created")

author_schema = AuthorSchema()
authors_schema = AuthorSchema(many=True)
        


# class AuthorSchema(ModelSchema):
#     class Meta(ModelSchema.Meta):
#         model = Author
#         sqla_session = db.session
#     id = fields.Number(dump_only=True)
#     first_name = fields.String(required=True)
#     last_name = fields.String(required=True)
#     created = fields.String(dump_only=True)
#     books = fields.Nested(BookSchema, many=True,only=['title','year','id'])