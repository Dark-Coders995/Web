from flask import Blueprint, redirect, session, url_for, flash
from flask import render_template, request

from models.database import db
from models.models import User, Category

routes = Blueprint('routes', __name__)


@routes.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(user_name=username).first()
        if user and user.password == password:
            session['user_id'] = user.user_id
            flash('Logged in successfully!', 'success')
            return redirect(url_for('routes.logged_in'))
        else:
            if user and user.password != password:
                return 'Invalid Password'
            if not user:
                return render_template('sign_up.html')
    return render_template('login.html')


@routes.route('/logged_user', methods=['GET', 'POST'])
def logged_in():
    if request.method == 'GET':
        if 'user_id' in session:
            user_id = session['user_id']
            user = User.query.get(user_id)
            categories = Category.query.all()
            return render_template("user/user_logged.html", user=user, categories=categories)
        else:
            return "Unauthorized access. Please log in first."


@routes.route('/manager_logged', methods=['GET', 'POST'])
def manager_logged():
    if request.method == 'GET':
        if 'user_id' in session:
            manager_id = session['user_id']
            user = User.query.get(manager_id)
            categories = Category.query.all()
        return render_template("manager/manager_logged.html", user=user, categories=categories)
    else:
        return 'Unauthorized Login'


@routes.route('/manager_login', methods=['GET', 'POST'])
def manager_login():
    if request.method == 'POST':
        manager_username = request.form['manager_username']
        password = request.form['password']
        user = User.query.filter_by(user_name=manager_username).first()
        if user and user.password == password and user.is_active == 0:
            session['user_id'] = user.user_id
            flash('Logged in successfully!', 'success')
            return redirect(url_for('routes.manager_logged'))
        else:
            if user and user.password != password:
                return 'Invalid Password'
            if not user:
                return 'Invalid Admin'
    return render_template('manager_login.html')


@routes.route('/sign_up', methods=['GET', 'POST'])
def signup_login():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        new_user = User(user_name=name, email=email, password=password, is_active=1)
        db.session.add(new_user)
        db.session.commit()
        session['user_id'] = new_user.user_id
        return redirect(url_for('routes.logged_in'))

    return render_template('sign_up.html')
