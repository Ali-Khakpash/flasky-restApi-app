from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
db = SQLAlchemy()
ma = Marshmallow()

#the reason why we created a separate db file is that this file creates just
#one instance of SQLAlchemy so that we can make relation between our models 