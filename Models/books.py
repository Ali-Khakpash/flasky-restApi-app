from flask_sqlalchemy import SQLAlchemy
from db import db
#from app import db


class Book(db.Model):
    __tablename__ = 'books'
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    title = db.Column(db.String(50))
    year = db.Column(db.Integer)
    # author_id = db.Column(db.Integer, db.ForeignKey('authors.id'))
    # authors = db.relationship('Author', backref=db.backref('books', lazy='dynamic'))
    author_id = db.Column(db.Integer, db.ForeignKey('authors.id'))

    def __init__(self, title, year, author_id=None):
        self.title = title
        self.year = year
        self.author_id = author_id


# class BookSchema(ModelSchema):
#     class Meta(ModelSchema.Meta):
#         model = Book
#         sqla_session = db.session
#     id = fields.Number(dump_only=True)
#     title = fields.String(required=True)
#     year = fields.Integer(required=True)
#     author_id = fields.Integer()