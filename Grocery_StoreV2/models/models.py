from models.database import db


class User(db.Model):
    user_id = db.Column(db.Integer, primary_key=True, unique=True, autoincrement=True)
    user_name = db.Column(db.String(150))
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    is_active = db.Column(db.Boolean())
    carts = db.relationship('Cart', backref='user', lazy=True)

    def __repr__(self):
        return f"User({self.user_name}, {self.email})"


class Category(db.Model):
    category_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    category_name = db.Column(db.String(150))
    products = db.relationship('Product', backref='category', lazy=True, cascade='all, delete-orphan')

    def __repr__(self):
        return f"Category({self.category_name})"


class Product(db.Model):
    product_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    product_name = db.Column(db.String(150))
    rate = db.Column(db.Integer)
    quantity = db.Column(db.Integer)
    unit = db.Column(db.String(150))
    cat_id = db.Column(db.Integer, db.ForeignKey('category.category_id', ondelete='CASCADE'), nullable=False)

    def __repr__(self):
        return f"Product({self.product_name}, {self.rate} , {self.unit} , {self.quantity})"


class Cart(db.Model):
    cart_id = db.Column(db.Integer, primary_key=True, unique=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.product_id'))
    quantity = db.Column(db.Integer, nullable=False)
    total_price = db.Column(db.Float, nullable=False)
    product = db.relationship('Product', backref='carts', lazy=True)
