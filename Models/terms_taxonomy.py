from db import db,ma
from marshmallow_sqlalchemy import ModelSchema
from marshmallow import fields
from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey, BIGINT


class Terms_Taxonomy(db.Model):
    __tablename__ = 'terms_taxonomy'
    #when defining ForeignKey, the type of 2 columns must be the same.
    term_taxonomy_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    term_id = db.Column(db.Integer, db.ForeignKey('terms.term_id'))
    taxonomy = db.Column(db.VARCHAR(32))
    parent = db.Column(db.BIGINT(), nullable=True)

    def __init__(self, term_id, taxonomy, parent=None):
        self.term_id = term_id
        self.taxonomy = taxonomy
        self.parent = parent


class TermsTaxonomySchema(ModelSchema):
    class Meta(ModelSchema.Meta):
        model = Terms_Taxonomy
        sqla_session = db.session


term_taxonomy_schema = TermsTaxonomySchema()
terms_taxonomy_schema = TermsTaxonomySchema(many=True)
