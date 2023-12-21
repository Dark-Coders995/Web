import jwt
from flask import jsonify, request
from flask_restful import Resource, reqparse
from flask_security import login_user
from config.validation import *
from models.models import User
from models.database import db
from config.security import user_datastore
from Caches.cache_api import get_category
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity


editcategory_parser = reqparse.RequestParser()
editcategory_parser.add_argument('name')
editcategory_parser.add_argument('description')

class AdminEditCategoryAPI(Resource):
    @jwt_required()
    def put(self, category_id):
        
        args = editcategory_parser.parse_args()
        name = args.get("name")
        description = args.get('description')


        category = get_category(category_id)
        if not category:
            return {'message': 'Category not found'}, 404

        category.name = name
        category.description = description

        db.session.commit()

        return {'message': 'Category updated successfully'}, 200


