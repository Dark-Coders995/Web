from flask_restful import Resource, reqparse, fields, marshal_with

from api.validation import BusinessValidationError
from models.database import db
from models.models import Product, Cart

buy_product = reqparse.RequestParser()
buy_product.add_argument("buy_quantity")

output_fields = {
    "product_id": fields.Integer,
    "product_name": fields.String,
    "quantity": fields.Integer,
    "rate": fields.Integer,
    "unit": fields.String,
    "category": {
        "category_name": fields.String(attribute=lambda product: product.category.category_name),
    }
}


class BuyResource(Resource):
    @marshal_with(output_fields)
    def get(self, product_id):
        product = Product.query.get(product_id)
        return product
        pass

    def post(self, product_id):
        args = buy_product.parse_args()
        buy_quantity = args.get("buy_quantity", None)
        buy = int(buy_quantity)
        product = Product.query.get(product_id)
        cart_item = Cart.query.filter_by(user_id=1, product_id=product_id).first()
        if buy > product.quantity:
            raise BusinessValidationError(status_code=404, error_code="BE101", error_message="Out of Stock")
        else:
            total_price = product.rate * buy
            product.quantity -= buy
            db.session.commit()
        if cart_item:
            cart_item.quantity += buy
            cart_item.total_price += total_price
        else:
            cart_item = Cart(user_id=1, product_id=product_id, quantity=buy, total_price=total_price)
            db.session.add(cart_item)
        db.session.commit()
        pass
