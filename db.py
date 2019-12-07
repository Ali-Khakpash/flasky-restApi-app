from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_jwt_extended import JWTManager
db = SQLAlchemy()
ma = Marshmallow()##note that Marshmallow can't handle Serilization Completely
                  ##and we also need to use marshmallow_sqlalchemy in the Model 
                  ##for complete serilization
jwt = JWTManager()

#the reason why we created a separate db file is that this file creates just
#one instance of SQLAlchemy so that we can make relation between our models 