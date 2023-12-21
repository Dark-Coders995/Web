from flask import jsonify
from flask_restful import Resource
from models.models import Product  
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity
from Caches.cache_api import get_products_by_category
from api.Authentication.loginapi import user_required

class PostedProductsAPI(Resource):
    @jwt_required()
    @user_required
    def get(self, category_id):
        
        # Query the database to get all shows for the given venue_id
        products = get_products_by_category(category_id)

        products_data = [
            {
                'id': product.id,
                'name': product.name,
                'description': product.description,
                'price': product.price,
                'quantity': product.quantity,
            }
            for product in products
        ]

        return jsonify(products_data)