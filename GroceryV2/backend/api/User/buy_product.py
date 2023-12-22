from flask import jsonify
from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.models import *
from Caches.cache_api import get_product_by_productcategory , get_category
from api.Authentication.loginapi import user_required


book_parser = reqparse.RequestParser()
book_parser.add_argument('quantity', type=int)

# API resource for booking a show
# Remove the total_seats_booked property from the Show model

# BookShowAPI class
class BuyProductAPI(Resource):
    @jwt_required()
    @user_required
    def post(self, category_id, product_id):
        args = book_parser.parse_args()
        quantity = args.get('quantity')


        user_id = get_jwt_identity()


        category = get_category(category_id)

        if not category:
            return {'message': 'Category not found'}, 404


        product = get_product_by_productcategory(category_id, product_id)

        if not product:
            return {'message': 'Product not found'}, 404


        total_quantity_bought = product.total_cart

        available_quantity = product.quantity - total_quantity_bought
        if quantity > available_quantity:
            return {'message': 'Not enough available Products for booking'}, 400


        total = quantity * product.price


        cart= Cart(user_id=user_id, product_id=product_id, quantity=quantity, total = total)
        db.session.add(cart)


        product.quantity = available_quantity - quantity

        db.session.commit()

        return {'message': 'Booking successful', 'available_Products': product.quantity}, 200






