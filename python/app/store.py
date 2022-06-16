from flask import Blueprint

store = Blueprint('store', __name__)


@store.route('/cart')
def cart():
    return 'cart'

@store.route('/items')
def items():
    return 'items'

@store.route('/item')
def item():
    return 'single item'

@store.route('/sold_items')
def sold_items():
    return 'sold_items'