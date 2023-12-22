import secrets
from werkzeug.security import generate_password_hash, check_password_hash
from flask_restful import Resource, reqparse
from flask_security.utils import hash_password
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from datetime import timedelta
from flask import Flask, request, jsonify
def method_name():
    pass
from config.validation import  BusinessValidationError

from models.models import  User
from models.database import db



user_parser = reqparse.RequestParser()
user_parser.add_argument('username')
user_parser.add_argument('email')
user_parser.add_argument('password')

class SignupAPI(Resource):
    def post(self):
        args = user_parser.parse_args()
        username = args.get("username", None)
        email = args.get("email", None)
        password = args.get("password", None)

        if username is None:
            raise BusinessValidationError(status_code=400, error_code="BE1001", error_message="Please Enter Username!")
        if email is None:
            raise BusinessValidationError(status_code=400, error_code="BE1002", error_message="Please Enter Email!")
        if password is None:
            raise BusinessValidationError(status_code=400, error_code="BE1003", error_message="Please Enter Password!")
        
        user_namecheck = db.session.query(User).filter(User.username == username).first()
        user_mailcheck = db.session.query(User).filter(User.email == email).first()
            
        if user_namecheck:
            raise BusinessValidationError(status_code=400, error_code="BE105", error_message="Username already exists!")
        if not '@' in email:
            raise BusinessValidationError(status_code=400, error_code="BE104", error_message="Invalid email")
        if user_mailcheck:
            raise BusinessValidationError(status_code=400, error_code="BE106", error_message="Email Not Available!")

        # Check if there are any users in the database
        if db.session.query(User).count() > 0:
            new_user = User(username=username, email=email, password=hash_password(password), active=True, is_admin=False)
            new_user.fs_uniquifier = secrets.token_hex(16)

            db.session.add(new_user)
            db.session.commit()
            return {'status': 'success', 'message': 'SignUp Successful!'}
        else:
            return {'message': 'App needs an admin first', 'alert': 'Please note that there are no users in the database. You need an admin to sign up first.'}
