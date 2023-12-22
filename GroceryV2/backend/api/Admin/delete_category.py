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
from Caches.cache_api import get_category

class AdminDeleteCategoryAPI(Resource):
    @jwt_required()
    @admin_required
    def delete(self, category_id):
        category = get_category(category_id)
        if not category:
            return {'message': 'Category not found'}, 404
        
        products_to_delete = db.session.query(Product).filter(Product.category_id == category_id).all()
        product_ids = [product.id for product in products_to_delete]
        db.session.query(Cart).filter(Cart.product_id.in_(product_ids)).delete(synchronize_session=False)
        db.session.query(Product).filter(Product.id.in_(product_ids)).delete(synchronize_session=False)

        #db.session.query(product_ids).filter(Product.category_id == category_id).delete()

        db.session.delete(category)
        db.session.commit()

        return {'message': 'Category, associated Product, and bookings deleted'}, 200