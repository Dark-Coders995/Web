import re

from flask_restful import Resource, reqparse, fields, marshal_with
from werkzeug.security import generate_password_hash

from api.validation import BusinessValidationError
from jwt_token.auth_middleware import token_required
from models.database import db
from models.models import User

create_user_parser = reqparse.RequestParser()
create_user_parser.add_argument('user_name')
create_user_parser.add_argument('email')
create_user_parser.add_argument('password')
create_user_parser.add_argument('is_active', type=bool)

buy_product = reqparse.RequestParser();
buy_product.add_argument('buy_quantity')

output_fields = {
    "user_id": fields.Integer,
    "user_name": fields.String,
    "email": fields.String,
    "is_active": fields.Boolean,

}


def is_valid_email(email):
    # Regular expression pattern for validating an email address
    pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    return bool(re.match(pattern, email))


class UserResource(Resource):
    @marshal_with(output_fields)
    #@token_required
    def get(self, user_id):
        # Retrieve user data from the database and return as JSON
        user = User.query.get(user_id)

        if user:
            return user
        else:
            raise BusinessValidationError(status_code=404, error_code="BE101", error_message="User not found!")
        pass

    def post(self):
        args = create_user_parser.parse_args()
        username = args.get("user_name", None)
        email = args.get("email", None)
        password = args.get("password", None)

        if username is None:
            raise BusinessValidationError(status_code=650, error_code="BE1001", error_message="username is required")

        if email is None:
            raise BusinessValidationError(status_code=651, error_code="BE1002", error_message="email is required")

        if password is None:
            raise BusinessValidationError(status_code=652, error_code="BE1003", error_message="password is required")

        user1 = db.session.query(User).filter(User.user_name == username).first()

        user2 = db.session.query(User).filter(User.email == email).first()

        if user1:
            raise BusinessValidationError(status_code=653, error_code="BE105", error_message="Username already exists")

        if not is_valid_email(email):
            raise BusinessValidationError(status_code=654, error_code="BE104", error_message="Invalid email")

        if user2:
            raise BusinessValidationError(status_code=655, error_code="BE106", error_message="Email already in use")

        new_user = User(user_name=username, email=email, is_active=1,
                        password=generate_password_hash(password, method='sha256'))
        db.session.add(new_user)
        db.session.commit()
        return "", 201
        # Create a new user in the database and return the created user as JSON

    def put(self, user_id):
        args = create_user_parser.parse_args()
        # Update user data in the database and return the updated user as JSON
        pass

    def delete(self, user_id):
        # Delete a user from the database and return a message
        pass
