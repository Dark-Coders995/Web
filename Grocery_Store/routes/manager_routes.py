from flask import Blueprint, redirect
from flask import render_template, request

from models.database import db
from models.models import Category, Product

manager_routes = Blueprint('manager_routes', __name__)


@manager_routes.route('/add_category', methods=['GET', 'POST'])
def add_category():
    if request.method == 'POST':
        category_name = request.form["category_name"]
        if category_name is None:
            return "Enter valid category"
        try:
            category = Category(category_name=category_name)
            db.session.add(category)
            db.session.commit()
            return redirect('/manager_logged')
        except Exception as e:
            print(e)
            return "Please try again later."
    return render_template('manager/add_category.html')


@manager_routes.route('/delete_category/<int:category_id>', methods=['POST'])
def delete_category(category_id):
    try:
        category = Category.query.get(category_id)
        if category:
            db.session.delete(category)
            db.session.commit()
        else:
            return "Category not found."
    except Exception as e:
        print(e)
        return "Error occurred while deleting the category. Please try again later."
    return redirect('/manager_logged')


@manager_routes.route('/update_category/<int:category_id>', methods=['GET', 'POST'])
def update_category(category_id):
    category = Category.query.get(category_id)
    if not category:
        return "Category not found."

    if request.method == 'POST':
        new_category_name = request.form["new_category_name"]
        if not new_category_name:
            return "Enter a valid category name."

        try:
            category.category_name = new_category_name
            db.session.commit()
            return redirect('/manager_logged')
        except Exception as e:
            print(e)
            return "Error occurred while updating the category. Please try again later."

    return render_template('manager/update_category.html', category_id=category_id)


@manager_routes.route('/add_product/<int:category_id>', methods=['GET', 'POST'])
def add_product(category_id):
    category = Category.query.get(category_id)
    if not category:
        return "Category not found."

    if request.method == 'POST':
        product_name = request.form.get('product_name')
        rate = request.form.get('rate')
        quantity = request.form.get('quantity')
        unit = request.form.get('unit')

        if not all([product_name, rate, quantity, unit]):
            return "Please fill in all the product details."

        try:
            product = Product(product_name=product_name, rate=rate, quantity=quantity, unit=unit, cat_id=category_id)
            db.session.add(product)
            db.session.commit()
            return redirect('/manager_logged')
        except Exception as e:
            print(e)
            return "Error occurred while adding the product. Please try again later."

    return render_template('manager/add_product.html', category=category)


@manager_routes.route('/update_product/<int:product_id>', methods=['GET', 'POST'])
def update_product(product_id):
    product = Product.query.get(product_id)
    if not product:
        return "Product not found."

    if request.method == 'POST':
        new_product_name = request.form.get('new_product_name')
        new_rate = request.form.get('new_rate')
        new_quantity = request.form.get('new_quantity')
        new_unit = request.form.get('new_unit')

        if not all([new_product_name, new_rate, new_quantity, new_unit]):
            return "Please fill in all the product details."

        try:
            product.product_name = new_product_name
            product.rate = new_rate
            product.quantity = new_quantity
            product.unit = new_unit
            db.session.commit()
            return redirect('/manager_logged')
        except Exception as e:
            print(e)
            return "Error occurred while updating the product. Please try again later."

    return render_template('manager/update_product.html', product=product)


@manager_routes.route('/delete_product/<int:product_id>', methods=['POST'])
def delete_product(product_id):
    try:
        product = Product.query.get(product_id)
        if product:
            db.session.delete(product)
            db.session.commit()
        else:
            return "Product not found."
    except Exception as e:
        print(e)
        return "Error occurred while deleting the product. Please try again later."
    return redirect('/manager_logged')
