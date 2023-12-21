from flask import Blueprint, request, render_template, redirect, session, url_for

from models.database import db
from models.models import Product, Cart, User

user_routes = Blueprint('user_routes', __name__)


@user_routes.route('/buy/<int:product_id>', methods=['GET', 'POST'])
def buy(product_id):
    product = Product.query.get(product_id)
    user_id = session['user_id']
    cart_item = Cart.query.filter_by(user_id=user_id, product_id=product_id).first()
    if request.method == 'POST':
        buy_quantity = int(request.form['buy_quantity'])
        if buy_quantity > product.quantity:
            return "Out of stock. Please enter a quantity less than or equal to the available quantity."
        else:
            total_price = product.rate * buy_quantity
            product.quantity -= buy_quantity
            db.session.commit()
        if cart_item:
            cart_item.quantity += buy_quantity
            cart_item.total_price += total_price
        else:
            cart_item = Cart(user_id=user_id, product_id=product_id, quantity=buy_quantity, total_price=total_price)
            db.session.add(cart_item)
        db.session.commit()

        return redirect(url_for('routes.logged_in'))

    return render_template('user/buy.html', product=product)


@user_routes.route('/cart', methods=['GET', 'POST'])
def cart():
    user_id = session['user_id']
    user = User.query.get(user_id)

    if request.method == 'POST':
        action = request.form.get('action')
        if action == 'remove':
            cart_item_id = request.form.get('cart_item_id')
            if cart_item_id:
                cart_item_id = int(cart_item_id)
                cart_item = Cart.query.get(cart_item_id)
                product = cart_item.product
                product.quantity += cart_item.quantity
                db.session.delete(cart_item)
                db.session.commit()
        return redirect(url_for('user_routes.cart'))

    cart_items = Cart.query.filter_by(user_id=user_id).all()
    total_price = sum(item.total_price for item in cart_items)

    return render_template('user/cart.html', user=user, cart_items=cart_items, total_price=total_price)


@user_routes.route('/update_cart/<int:product_id>', methods=['GET', 'POST'])
def update_cart(product_id):
    user_id = session['user_id']
    product = Product.query.get(product_id)
    cart_item = Cart.query.filter_by(user_id=user_id, product_id=product_id).first()
    if request.method == 'POST':
        if cart_item:
            current_cart_quantity = cart_item.quantity
        else:
            current_cart_quantity = 0
        update = request.form['update_quantity']
        new_quantity = int(update)
        available_quantity = product.quantity

        if new_quantity < current_cart_quantity:
            quantity_difference = current_cart_quantity - new_quantity
            if available_quantity >= quantity_difference:
                if cart_item:
                    cart_item.quantity = new_quantity
                else:
                    cart_item = Cart(user_id=user_id, product_id=product_id, quantity=new_quantity, total_price=0)
                    db.session.add(cart_item)
                product.quantity += quantity_difference
                db.session.commit()
        elif new_quantity > current_cart_quantity:
            quantity_difference = new_quantity - current_cart_quantity
            if available_quantity >= quantity_difference:
                if cart_item:
                    cart_item.quantity = new_quantity
                else:
                    cart_item = Cart(user_id=user_id, product_id=product_id, quantity=new_quantity, total_price=0)
                    db.session.add(cart_item)
                product.quantity -= quantity_difference
                db.session.commit()
        else:
            pass
        return redirect(url_for('user_routes.cart'))
    return render_template('user/update_cart.html', product=product)
