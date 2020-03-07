from db import db
from flask_authorize import AllowancesMixin


class Role(db.Model, AllowancesMixin):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False, unique=True)

    def __init__(self, name):
        self.name = name

