from models.models import Category, Product
from Caches.cache import cache
from flask_jwt_extended import jwt_required


@jwt_required()
@cache.cached(timeout=10, key_prefix='get_all_venues')
def get_all_category():
    category = Category.query.all()
    return category

@jwt_required()
@cache.memoize(10)
def get_products_by_category(category_id):
    products = Product.query.filter_by(category_id=category_id)
    return products.all()

@jwt_required()
@cache.memoize(10)
def get_category(category_id):
    category = Category.query.get(category_id)
    return category

@jwt_required()
@cache.memoize(10)
def get_product_by_productcategory(category_id, product_id):
    product = Product.query.filter_by(id=product_id, category_id=category_id)
    return product.first()