import jwt
from flask import jsonify
from flask_restful import Resource, reqparse
from flask_security import login_user
from flask_security.utils import verify_password
from config.validation import *
from models.models import *
from models.database import db
from config.security import user_datastore
from api.Authentication.adminlogin import admin_required
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity
from Caches.cache_api import  get_products_by_category



product_parser = reqparse.RequestParser()
product_parser.add_argument('name', type=str, required=True)
product_parser.add_argument('description', type=str, required=True)
product_parser.add_argument('price', type=int, required=True)
product_parser.add_argument('quantity', type=int, required=True)

class AdminAddProductAPI(Resource):
    @jwt_required()
    @admin_required
    def post(self, category_id):
        args = product_parser.parse_args()

        
        name = args['name']
        description = args['description']
        price = args['price']
        quantity = args['quantity']

        new_product = Product(
            name=name,
            description=description,
            price=price,
            quantity=quantity,
            category_id=category_id
        )

       
        db.session.add(new_product)
        db.session.commit()

       
        return {'message': 'Product created successfully', 'product_id': new_product.id}, 201

   

class AdminGetProductAPI(Resource):
    @jwt_required()
    @admin_required
    def get(self, category_id):
        products = get_products_by_category(category_id)

        product_list = []
        for product in products:
            product_data = {
                'id': product.id,
                'name': product.name,
                'description': product.description,
                'price': product.price,
                'quantity': product.quantity,
                'category_id': product.category_id
            }
            product_list.append(product_data)

        return {'Products': product_list}, 200