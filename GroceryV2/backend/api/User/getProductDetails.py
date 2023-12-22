from flask import jsonify, request
from flask_restful import Resource
from models.models import *
from models.database import db
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity
from Caches.cache_api import  get_product_by_productcategory
from api.Authentication.loginapi import user_required

class ProductDetailAPI(Resource):
    @jwt_required()
    @user_required
    def get(self, category_id, product_id):
        product = get_product_by_productcategory(category_id, product_id)
        if product:
            product_data = {
                'id': product.id,
                'name': product.name,
                'price': product.price,
                'description': product.description,
                'quantity': product.quantity,
                'category_id': product.category_id
            }
            return product_data, 200
        return jsonify({'message': 'Product  not found'}), 404