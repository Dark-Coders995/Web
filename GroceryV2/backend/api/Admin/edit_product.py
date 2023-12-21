import jwt
from flask import jsonify
from flask_restful import Resource, reqparse
from flask_security import login_user
from flask_security.utils import verify_password
from config.validation import *
from models.models import *
from config.security import user_datastore
from api.Authentication.adminlogin import admin_required
from models.database import db
from Caches.cache_api import get_product_by_productcategory
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity



product_parser = reqparse.RequestParser()
product_parser.add_argument('name', type=str, required=True)
product_parser.add_argument('description', type=str, required=True)
product_parser.add_argument('price', type=float, required=True)
product_parser.add_argument('quantity', type=int, required=True)

class AdminEditProductAPI(Resource):
    @jwt_required()
    @admin_required
    def put(self, category_id, product_id):
        args = product_parser.parse_args()

        product = get_product_by_productcategory(category_id, product_id)
        if not product:
            return {'message': 'Product not found'}, 404

        product.name = args['name']
        product.description = args['description']
        product.price = args['price']
        product.quantity = args['quantity']

        db.session.commit()

        return {'message': 'Product updated successfully'}, 200