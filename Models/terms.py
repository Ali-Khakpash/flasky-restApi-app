from db import db,ma
from marshmallow_sqlalchemy import ModelSchema
from marshmallow import fields

class Terms(db.Model):
    __tablename__ = 'terms'
    term_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.VARCHAR(200))

    def __init__(self, name):
        self.name = name


class TermsSchema(ModelSchema):
    class Meta(ModelSchema.Meta):
        model = Terms
        sqla_session = db.session

term_schema = TermsSchema()
terms_schema = TermsSchema(many=True)
