from flask_security import Security, SQLAlchemyUserDatastore
from models.database import db
from models.models import User, Role

user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security()
