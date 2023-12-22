from flask import request
from flask_restful import Resource, reqparse, fields, marshal_with
from api.validation import BusinessValidationError

from models.database import db
from models.models import Category, Product

add_product = reqparse.RequestParser()
add_product.add_argument('product_name')
add_product.add_argument('quantity')
add_product.add_argument('rate')
add_product.add_argument('unit')

output_fields = {
    "product_id": fields.Integer,
    "product_name": fields.String,
    "quantity": fields.Integer,
    "rate": fields.Integer,
    "unit": fields.String
}


class ProductResource(Resource):
    @marshal_with(output_fields)
    def get(self):
        # Retrieve category data from the database and return as JSON
        product = Product.query.all()

        if product:
            return product
        else:
            raise BusinessValidationError(status_code=404, error_code="BE101", error_message="Category not found!")
        pass

    def post(self, category_id):
        category = Category.query.get(category_id)
        if not category:
            raise BusinessValidationError(status_code=704, error_code="BE101", error_message="Category not found!")
        args = add_product.parse_args()
        product_name = args.get("product_name", None)
        rate = args.get("rate", None)
        quantity = args.get("quantity", None)
        unit = args.get("unit", None)
        if product_name is None:
            raise BusinessValidationError(status_code=750, error_code="BE105",
                                          error_message="Product name is required")
        if rate is None:
            raise BusinessValidationError(status_code=751, error_code="BE104",
                                          error_message="Rate is required")
        if quantity is None:
            raise BusinessValidationError(status_code=752, error_code="BE106",
                                          error_message="Quantity is required")

        new_product = Product(product_name=product_name, rate=rate, quantity=quantity, unit=unit, cat_id=category_id)
        db.session.add(new_product)
        db.session.commit()
        return "", 201
        # Create a new user in the database and return the created user as JSON

    @marshal_with(output_fields)
    def put(self, product_id):
        product = Product.query.get(product_id)
        if not product:
            raise BusinessValidationError(status_code=704, error_code="BE101", error_message="Product not found!")

        args = add_product.parse_args()
        new_name = args.get("product_name", None)
        new_rate = args.get("rate", None)
        new_quantity = args.get("quantity", None)
        new_unit = args.get("unit", None)

        product.product_name = new_name
        product.rate = new_rate
        product.quantity = new_quantity
        product.unit = new_unit
        db.session.commit()
        return product
        pass

    def delete(self, product_id):
        product = Product.query.get(product_id)
        if not product:
            raise BusinessValidationError(status_code=704, error_code="BE101", error_message="Product not found!")
        else:
            db.session.delete(product)
            db.session.commit()
        pass
