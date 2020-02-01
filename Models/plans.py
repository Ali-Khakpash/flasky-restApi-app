from db import db,ma
from flask_sqlalchemy import SQLAlchemy
from marshmallow_sqlalchemy import ModelSchema
from marshmallow import fields
#from app import db


class Plan(db.Model):
    __tablename__ = 'plans'
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    title = db.Column(db.String(50))
    short_desc = db.Column(db.String(300))
    time_created = db.Column(db.DateTime, server_default=db.func.now())
    time_updated = db.Column(db.DateTime, nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __init__(self, name, desc, user_id=None):
        self.name = name
        self.desc = desc
        self.user_id = user_id


class PlanSchema(ModelSchema):
    class Meta(ModelSchema.Meta):
        model = Plan
        sqla_session = db.session
    id = fields.Number(dump_only=True)
    name = fields.String(required=True)
    desc = fields.String(required=True)
    user_id = fields.Integer()

paln_schema = PlanSchema()
plans_schema = PlanSchema(many=True)