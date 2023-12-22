from flask import Blueprint
from flask_restful import Api

from api.buy_api import BuyResource
from api.cart_api import CartResource
from api.categories_api import CategoryResource
from api.user_api import UserResource

user = Blueprint('user', __name__)
user_api = Api(user)

user_api.add_resource(UserResource, '/user/sign_up')
user_api.add_resource(CategoryResource, '/category')
user_api.add_resource(CartResource, '/cart')
user_api.add_resource(BuyResource, '/buy/<int:product_id>')
