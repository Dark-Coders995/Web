from flask import Blueprint
from flask_restful import Api
from api.categories_api import CategoryResource
from api.products_api import ProductResource

manager = Blueprint('manager', __name__)
manager_api = Api(manager)

manager_api.add_resource(CategoryResource, '/manager/update_category/<int:category_id>', '/manager/add_category',
                         '/manager/delete_category/<int:category_id>')

manager_api.add_resource(ProductResource, '/manager/add_product/<int:category_id>',
                         '/manager/update_product/<int:product_id>', '/manager/delete_product/<int:product_id>')
