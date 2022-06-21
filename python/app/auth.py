from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_user, login_required, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from .models import User

auth = Blueprint('auth', __name__)


@auth.route('/login')
def login():
    """
    Login page endpoint
    :return: HTML page
    """
    return render_template('login.html')


@auth.route('/login', methods=['POST'])
def login_post():
    """
    Login post endpoint. Checks if the user exists and if the password is correct.
    It is then redirected to the login page.
    :return: HTML page
    """
    email = request.form.get('email')
    password = request.form.get('password')
    remember = request.form.get('remember', False, type=bool)

    user = User.query.filter_by(email=email).first()

    # check if the user actually exists
    # take the user-supplied password, hash it, and compare it to the hashed password in the database
    if not user or not check_password_hash(user.password, password):
        flash('Please check your login details and try again.')
        return redirect(url_for('auth.login'))

    login_user(user, remember=remember)
    return redirect(url_for('main.index'))


@auth.route('/signup')
def signup():
    """
    Signup page endpoint.
    :return: HTML page
    """
    return render_template('signup.html')


@auth.route('/signup', methods=['POST'])
def signup_post():
    """
    Signup post endpoint. If the user already exists, they are redirected to the login page.
    If the user does not exist, they are added to the database and then redirected to the login page.
    Parameters are taken from the form on the signup page.
    :return: HTML page
    """
    email = request.form.get('email')
    name = request.form.get('name')
    password = request.form.get('password')
    usertype = request.form.get('usertypeRadio')

    user = User.query.filter_by(
        email=email).first()

    if user:
        flash('Email address already exists')
        return redirect(url_for('auth.signup'))

    # create a new user with the form data. Hash the password so the plaintext version isn't saved.
    new_user = User(email=email, name=name, password=generate_password_hash(password, method='sha256'),
                    usertype=usertype)

    # add the new user to the database
    db.session.add(new_user)
    db.session.commit()
    return redirect(url_for('auth.login'))


@auth.route('/logout')
@login_required
def logout():
    """
    Logout endpoint. Logs the user out and redirects to the main page.
    :return: HTML page
    """
    logout_user()
    return redirect(url_for('main.index'))
