from flask import jsonify, request
from flask_restful import Resource
from models.models import * 
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity
from sqlalchemy import func
from api.Authentication.loginapi import user_required


class SearchCategoryAPI(Resource):
    @jwt_required()
    @user_required
    def get(self):
        name = request.args.get('name')

        if not name:
            return jsonify({'message': 'name parameter is missing'}), 400
        categories = Category.query.filter(Category.name.like(f'%{name}%')).all()

        if not categories:
            return jsonify({'message': 'No categories found'}), 404

        category_list = []
        for category in categories:
            category_data = {
                'id': category.id,
                'name': category.name,
                'description': category.description,
                'products': category.products
            }
            category_list.append(category_data)

        return category_list, 200
    
class SearchProductAPI(Resource):
    @jwt_required()
    @user_required
    def get(self):
        name = request.args.get('name')

        if not name:
            return jsonify({'message': 'name parameter is missing'}), 400
        products = Product.query.filter(Product.name.like(f'%{name}%')).all()

        if not products:
            return jsonify({'message': 'No Product found'}), 404

        products_list = []
        for product in products:
            product_data = {
                'id': product.id,
                'name': product.name,
                'items': product.items
            }
            products_list.append(product_data)

        return products_list, 200