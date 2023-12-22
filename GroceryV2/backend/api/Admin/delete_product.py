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
from Caches.cache_api import get_all_category, get_category, get_products_by_category, get_product_by_productcategory
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity


class AdminDeleteProductAPI(Resource):
    @jwt_required()
    @admin_required
    def delete(self, category_id, product_id):
        product = get_product_by_productcategory(category_id, product_id)
        if not product:
            return {'message': 'Product not found'}, 404
        
        db.session.query(Cart).filter(Cart.product_id == product_id).delete()

        db.session.delete(product)
        db.session.commit()

        return {'message': 'Product deleted successfully'}, 200