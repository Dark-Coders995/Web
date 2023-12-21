from flask import jsonify, request
from flask_restful import Resource
from models.models import *
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity
from api.Authentication.loginapi import user_required

def get_bought_product(product_id):
    bought_product = db.session.query(db.func.sum(Cart.quantity)).filter_by(product_id=product_id).scalar()
    return bought_product if bought_product else 0

class GetProductAPI(Resource):
    @jwt_required()
    @user_required
    def get(self, product_id):
        product = Product.query.get(product_id)
        if not product:
            return jsonify({'error': 'Product not found'}), 404

        bought_product = get_bought_product(product_id)
        available_products = product.quantity - bought_product

        return jsonify({'available_product': available_products})