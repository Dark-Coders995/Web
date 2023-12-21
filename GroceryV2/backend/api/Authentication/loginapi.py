import jwt
from functools import wraps
from flask import jsonify
from flask_restful import Resource, reqparse
from flask_security import login_user
from flask_security.utils import verify_password
from config.validation import *
from models.models import User
from models.database import db
from config.security import user_datastore

from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity, verify_jwt_in_request
from datetime import timedelta

user_parser = reqparse.RequestParser()
user_parser.add_argument('username')
user_parser.add_argument('password')

class LoginAPI(Resource):
	def post(self):
		args = user_parser.parse_args()
		username = args.get('username')
		password = args.get('password')
		user = None
		if '@' in username:
			user = db.session.query(User).filter(User.email == username).first()
		else:
			user = db.session.query(User).filter(User.username == username).first()
		
		if user:
			if not user.is_admin :

				if verify_password(password, user.password):

					access_token = create_access_token(identity=user.id, expires_delta=timedelta(seconds=1200))
					login_user(user)
				else:
				# return 404 error
					raise BusinessValidationError(status_code=404, error_code="BE102", error_message="Incorrect password!")
			else:
				raise BusinessValidationError(status_code=404, error_code="BE102", error_message="Only users are allowed!")
		else:
			raise BusinessValidationError(status_code=404, error_code="BE101", error_message="User not found!")
		
		return jsonify({'status': 'success','message': 'loggin Successfull !!', 'access_token': access_token, "username": username})
	

def user_required(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        verify_jwt_in_request()  # Verify JWT token in the request

        user_id = get_jwt_identity()  # Get the user ID from the JWT token
        user = User.query.get(user_id)  # Fetch the user object from the database

        if not user or user.is_admin:
            return jsonify(message="User required"), 403

        return func(*args, **kwargs)

    return decorated_function