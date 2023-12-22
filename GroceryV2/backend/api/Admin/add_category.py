import jwt
from flask import jsonify
from api.Authentication.adminlogin import admin_required
from flask_restful import Resource, reqparse
from flask_security import login_user
from flask_security.utils import verify_password
from config.validation import *
from models.models import User, Category
from models.database import db
from config.security import user_datastore
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from Caches.cache_api import get_all_category
addcategory_parser = reqparse.RequestParser()
addcategory_parser.add_argument('name')
addcategory_parser.add_argument('description')

class AdminAddCategoryAPI(Resource): 
    @jwt_required()
    @admin_required
    def post(self):
        args = addcategory_parser.parse_args()
        name = args.get("name", None)
        description = args.get("description", None)
        
        new_category = Category(name=name, description=description )
        db.session.add(new_category)
        db.session.commit()

        return {'message': 'Category added successfully'}, 201

class AdminGetCategoryAPI(Resource):
    @jwt_required()
    @admin_required
    
    def get(self):
        
        categories = get_all_category()

        categories_data = []
        for category in categories:
            category_data = {
                "id": category.id,
                "name": category.name,
                "description": category.description,
            }
            categories_data.append(category_data)

        return categories_data, 200