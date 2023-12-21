from flask import jsonify, request
from flask_restful import Resource
from models.models import *
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity
from api.Authentication.loginapi import user_required

class BuyDashAPI(Resource):
    @jwt_required()
    @user_required
    def get(self):
        user_id = get_jwt_identity()
        user = User.query.get(user_id)

        if not user:
            return jsonify({'message': 'User not found'}), 404

        carts = Cart.query.filter_by(user_id=user_id).all()
        user_bookings = []

        for cart_tems in carts:
            product = Product.query.get(cart_tems.product_id)
            category = Category.query.get(product.category_id)
            
            user_booking = {
                'cart_id': cart_tems.id,
                'Product_name': product.name,
                'category_name': category.name,
                'product_price': product.price,
                'quantity': cart_tems.quantity,
                'total': cart_tems.total,
            }
            user_bookings.append(user_booking)

        return user_bookings, 200