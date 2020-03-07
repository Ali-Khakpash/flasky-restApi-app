from db import db,ma
from Models.terms_taxonomy import Terms_Taxonomy, TermsTaxonomySchema
from marshmallow_sqlalchemy import ModelSchema
from marshmallow import fields
from flask_authorize import OwnerPermissionsMixin
from flask_sqlalchemy import SQLAlchemy
from Models.terms import TermsSchema


PlanTaxonomy = db.Table(
    'plan_taxonomy', db.Model.metadata,
    db.Column('plan_id', db.Integer, db.ForeignKey('plans.id')),
    db.Column('term_taxonomy_id', db.Integer, db.ForeignKey('terms_taxonomy.term_taxonomy_id'))
)




class Plan(db.Model, OwnerPermissionsMixin):
    __tablename__ = 'plans'
    __permissions__ = dict(
        owner=['read', 'update', 'delete', 'revoke'],
    )
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    title = db.Column(db.String(50))
    short_desc = db.Column(db.String(300))
    time_created = db.Column(db.DateTime, server_default=db.func.now())
    time_updated = db.Column(db.DateTime, nullable=True)

    plan_taxonomy = db.relationship('Terms_Taxonomy', secondary=PlanTaxonomy, backref=db.backref('term_taxonomy_plan', lazy='dynamic'))

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
    #plan_taxonomy = fields.Nested(TermsSchema, many=True, only=['name'])

paln_schema = PlanSchema()
plans_schema = PlanSchema(many=True)



