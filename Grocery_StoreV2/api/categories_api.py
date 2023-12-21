from flask import request
from flask_restful import Resource, reqparse, fields, marshal_with
from api.validation import BusinessValidationError

from models.database import db
from models.models import Category, Product

add_category = reqparse.RequestParser();
add_category.add_argument('category_name')

output_fields = {
    "category_id": fields.Integer,
    "category_name": fields.String,
    "products": fields.List(fields.Nested({
        "product_id": fields.Integer,
        "product_name": fields.String,
        "quantity": fields.Integer,
        "rate": fields.Integer,
        "unit": fields.String
    }))

}


class CategoryResource(Resource):
    @marshal_with(output_fields)
    def get(self):
        # Retrieve category data from the database and return as JSON
        category = Category.query.all()

        if category:
            return category
        else:
            raise BusinessValidationError(status_code=404, error_code="BE101", error_message="Category not found!")
        pass

    @marshal_with(output_fields)
    def put(self, category_id):
        category = Category.query.get(category_id)
        if not category:
            raise BusinessValidationError(status_code=704, error_code="BE101", error_message="Category not found!")

        args = add_category.parse_args()
        new_name = args.get("category_name", None)

        category.category_name = new_name
        db.session.commit()
        return category
        pass

    def post(self):
        args = add_category.parse_args()
        category_name = args.get("category_name", None)

        if category_name is None:
            raise BusinessValidationError(status_code=750, error_code="BE1001",
                                          error_message="Category name is required")

        new_cat = Category(category_name=category_name)
        db.session.add(new_cat)
        db.session.commit()
        return "", 201
        # Create a new user in the database and return the created user as JSON

    def delete(self, category_id):
        category = Category.query.get(category_id)
        if not  category:
            raise BusinessValidationError(status_code=704, error_code="BE101", error_message="Product not found!")
        else:
            db.session.delete(category)
            db.session.commit()
        pass
