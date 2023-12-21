import io
import base64
import matplotlib
matplotlib.use('Agg')  # Set the backend to 'Agg'
import matplotlib.pyplot as plt
from flask_restful import Resource
from models.models import *
from models.database import db
from flask_jwt_extended import jwt_required, get_jwt_identity
from api.Authentication.adminlogin import admin_required
from sqlalchemy import func

class SummaryAPI(Resource):

    @jwt_required()
    @admin_required
    def get(self):
        categories = Category.query.all()
        summary_data = []
        chart_images = []

        for category in categories:
            category_data = {
                'category_name': category.name,
                'products_data': []
            }
            products = Product.query.filter_by(category_id=category.id).all()
            for product in products:
                total = db.session.query(func.sum(Cart.quantity)).filter_by(product_id=product.id).scalar()
                if total is None:
                    total = 0

                product_data = {
                    'product_name': product.name,
                    'quantity': total
                }
                category_data['products_data'].append(product_data)

            summary_data.append(category_data)

        for category_data in summary_data:
            fig, ax = plt.subplots(figsize=(5, 4))
            product_names = [product_data['product_name'] for product_data in category_data['products_data']]
            quantity = [product_data['quantity'] for product_data in category_data['products_data']]
            name = category_data['category_name']
            ax.bar(product_names, quantity)
            ax.set_xlabel('Product  Name')
            ax.set_ylabel('Quantity Sold')
            ax.set_title(f'Quantity sold for {name}')

            buffer = io.BytesIO()
            plt.savefig(buffer, format='png')
            buffer.seek(0)
            image_base64 = base64.b64encode(buffer.read()).decode('utf-8')
            plt.close()

            chart_images.append('data:image/png;base64,' + image_base64)

        return {
            'summary_data': summary_data,
            'chart_images': chart_images
        }, 200
