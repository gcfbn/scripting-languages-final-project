import flask_login
from flask import Blueprint, render_template, request, flash, redirect, url_for

from .dao.store_dao import get_user_cart, remove_from_cart as dao_remove_from_cart, change_quantity_in_cart, \
    create_purchase, add_item_to_purchase, set_current_availability, get_single_item, add_to_cart as dao_add_to_cart, \
    already_in_cart, get_items, get_items_sold_by, update_item_price

store = Blueprint('store', __name__)


@store.route('/cart')
def cart():
    user_id = flask_login.current_user.id
    cart_items = get_user_cart(user_id)
    total_price = sum(i['ItemPrice'] * i['CartItemQuantity'] for i in cart_items)
    return render_template('cart.html', products=cart_items, total_items=len(cart_items), total_price=total_price)


@store.route('/items')
def items():
    items = get_items()
    return render_template('items.html', products=items)


@store.route('/items', methods=['POST'])
def items_post():
    query = request.form['search_bar']
    items = get_items(query)
    return render_template('items.html', products=items)


@store.route('/item')
def item():
    item_id = request.args.get('item_id')
    product = get_single_item(item_id)
    user_id = flask_login.current_user.id
    return render_template('item.html', product=product, already_in_cart=already_in_cart(item_id, user_id))


@store.route('/sold_items')
def sold_items():
    user_id = flask_login.current_user.id
    products = get_items_sold_by(user_id)
    return render_template('seller.html', products=products)


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
    user_id = flask_login.current_user.id
    cart_items = get_user_cart(user_id)
    purchase_id = create_purchase(user_id)
    for i in cart_items:
        add_item_to_purchase(purchase_id, i['ItemId'], i['CartItemQuantity'])
        set_current_availability(i['ItemAvailability'] - i['CartItemQuantity'], i['ItemId'])
        dao_remove_from_cart(user_id, i['ItemId'])
    flash('Purchase confirmed!')
    return redirect(url_for('store.cart'))


@store.route('/add_to_cart', methods=['POST'])
def add_to_cart():
    user_id = flask_login.current_user.id
    item_id = request.args.get('item_id')
    quantity = request.form['quantity']
    dao_add_to_cart(user_id, item_id, quantity)
    flash('Item added to cart.')
    return redirect(url_for('store.item', item_id=item_id))


@store.route('/change_price', methods=['POST'])
def change_price():
    item_id = request.args.get('item_id')
    new_price = request.form['new_price']
    update_item_price(new_price, item_id)
    flash('Price updated.')
    return redirect(url_for('store.sold_items'))


@store.route('/change_availability', methods=['POST'])
def change_availability():
    item_id = request.args.get('item_id')
    new_availability = request.form['new_availability']
    set_current_availability(new_availability, item_id)
    flash('Availability updated.')
    return redirect(url_for('store.sold_items'))


@store.route('/add_item')
def add_item():
    return render_template('add_item.html')