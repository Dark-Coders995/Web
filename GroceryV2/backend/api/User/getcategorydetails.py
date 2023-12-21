from flask import jsonify, request
from flask_restful import Resource
from models.models import Category
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity
from Caches.cache_api import get_category
from api.Authentication.loginapi import user_required

class CategoryDetailAPI(Resource):
    @jwt_required()
    @user_required
    def get(self, category_id):
        category = get_category(category_id)
        if category:
            category_data = {
                'id': category.id,
                'name': category.name,
                'description': category.description,
            }
            return category_data, 200
        return jsonify({'message': 'Venue not found'}), 404