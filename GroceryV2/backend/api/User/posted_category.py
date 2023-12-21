from flask import jsonify, request
from flask_restful import Resource
from models.models import Category  
from Caches.cache_api import get_all_category
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity
from api.Authentication.loginapi import user_required

class PostedCategoriesAPI(Resource):
    @jwt_required()
    @user_required
    def get(self):
        categories = get_all_category()

        categories_data = [
            {
                'id': category.id,
                'name': category.name,
                'description': category.description,
            }
            for category in categories
        ]

        return jsonify(categories_data)
