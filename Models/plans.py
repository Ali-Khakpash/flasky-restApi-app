from db import db,ma
from marshmallow_sqlalchemy import ModelSchema
from marshmallow import fields
from flask_authorize import PermissionsMixin
from flask_sqlalchemy import SQLAlchemy


class Plan(db.Model, PermissionsMixin):
    __tablename__ = 'plans'
    __permissions__ = dict(
        owner=['read', 'update', 'delete', 'revoke'],
        # group=['read', 'update'],
        group=['read', 'update'],
        other=['read']
    )
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    title = db.Column(db.String(50))
    short_desc = db.Column(db.String(300))
    time_created = db.Column(db.DateTime, server_default=db.func.now())
    time_updated = db.Column(db.DateTime, nullable=True)

    def __init__(self, title, short_desc, user_id=None):
        self.title = title
        self.short_desc = short_desc
        self.user_id = user_id


class PlanSchema(ModelSchema):
    class Meta(ModelSchema.Meta):
        model = Plan
        sqla_session = db.session
    #customized field
    number = fields.Number()
    # #customized field
    # since_created = fields.Method("get_days_since_created")
    #
    # def get_days_since_created(self, obj):
    #     return obj

paln_schema = PlanSchema()
plans_schema = PlanSchema(many=True)

