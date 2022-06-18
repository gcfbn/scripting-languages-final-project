import flask_login
from flask import Blueprint, render_template, request, flash, redirect, url_for

from .dao.store_dao import get_user_cart, remove_from_cart as dao_remove_from_cart, change_quantity_in_cart

store = Blueprint('store', __name__)


@store.route('/cart')
def cart():
    user_id = flask_login.current_user.id
    cart_items = get_user_cart(user_id)
    total_price = sum(i['ItemPrice'] * i['CartItemQuantity'] for i in cart_items)
    return render_template('cart.html', products=cart_items, total_items=len(cart_items), total_price=total_price)


@store.route('/items')
def items():
    return 'items'


@store.route('/item')
def item():
    return request.args.get('item_id')


@store.route('/sold_items')
def sold_items():
    return 'sold_items'


@store.route('/remove_from_cart')
def remove_from_cart():
    item_id = request.args.get('item_id')
    user_id = flask_login.current_user.id
    dao_remove_from_cart(user_id, item_id)
    flash('Item has been removed from cart')
    return redirect(url_for('store.cart'))


@store.route('/change_cart_quantity', methods=['POST'])
def change_cart_quantity():
    item_id = request.args.get('item_id')
    user_id = flask_login.current_user.id
    new_quantity = request.form['quantity']
    change_quantity_in_cart(new_quantity, item_id, user_id)
    flash('Quantity has been updated')
    return redirect(url_for('store.cart'))


@store.route('/buy')
def buy():
    user_id = flask_login.current_user.id
    cart_items = get_user_cart(user_id)
    total_price = sum(i['ItemPrice'] * i['CartItemQuantity'] for i in cart_items)
    return render_template('buy.html', total_items=len(cart_items), total_price=total_price, products=cart_items)


@store.route('/confirm_purchase')
def confirm_purchase():
    return 'purchase confirmed'
