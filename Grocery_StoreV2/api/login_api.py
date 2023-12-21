from datetime import datetime

import jwt
from flask import jsonify, current_app, request, make_response
from flask_restful import Resource
from werkzeug.security import check_password_hash

from api.validation import BusinessValidationError
from models.database import db
from models.models import User


class LoginAPI(Resource):
    def get(self, username, password):
        # Getting the User from the database based on the username
        user = None
        if '@' in username:
            user = db.session.query(User).filter(User.email == username).first()
        else:
            user = db.session.query(User).filter(User.user_name == username).first()

        if user:
            if check_password_hash(user.password, password):
                token = jwt.encode({'public_id': user.user_id, }, current_app.config['SECRET_KEY'], "HS256")
                print(type(current_app.config['SECRET_KEY']))
                return jsonify({'token': token})
            else:
                # return 404 error
                raise BusinessValidationError(status_code=568, error_code="BE102", error_message="Incorrect password!")
        else:
            raise BusinessValidationError(status_code=754, error_code="BE101", error_message="User not found!")
        pass
