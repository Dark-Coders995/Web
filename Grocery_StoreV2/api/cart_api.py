from flask_restful import Resource, reqparse, fields, marshal_with

from api.validation import BusinessValidationError
from models.database import db
from models.models import Product, Cart

buy_product = reqparse.RequestParser()
buy_product.add_argument("buy_quantity")
output_fields = {
    "cart_id": fields.Integer,
    "product": {
        "product_id": fields.Integer,
        "product_name": fields.String,
        "quantity": fields.Integer,
        "rate": fields.Integer,
        "unit": fields.String
    },
    "quantity": fields.Integer,
    "total_price": fields.Integer
}


class CartResource(Resource):
    def get(self):
        cart_items = Cart.query.filter_by(user_id=1).all()

        return cart_items
        pass

    def post(self, product_id):

        pass
