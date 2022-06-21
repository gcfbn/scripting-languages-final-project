from flask_login import login_required, current_user
from flask import Blueprint, render_template, request, flash, redirect, url_for

from .dao.store_dao import get_user_cart, remove_from_cart as dao_remove_from_cart, change_quantity_in_cart, \
    create_purchase, add_item_to_purchase, set_current_availability, get_single_item, add_to_cart as dao_add_to_cart, \
    already_in_cart, get_items, get_items_sold_by, update_item_price, add_product, delete_item as dao_delete_item, \
    get_seller_report, get_purchased_items
from .utils import groupby

store = Blueprint('store', __name__)


@store.route('/cart')
@login_required
def cart():
    """
    Displays the current user's cart. Takes current user's id from the session and queries
    the database for items in their cart.
    Calculates the total price and then renders html cart page.
    :return: HTML page
    """
    user_id = current_user.id
    cart_items = get_user_cart(user_id)
    total_price = sum(i['ItemPrice'] * i['CartItemQuantity'] for i in cart_items)
    return render_template('cart.html', products=cart_items, total_price=total_price)


@store.route('/items')
def items():
    """
    Displays all items in the store. Queries the database for all the items and then renders
    the html page.
    :return: HTML page
    """
    items = get_items()
    return render_template('items.html', products=items)


@store.route('/items', methods=['POST'])
def items_post():
    """
    Handles POST request from the items page. It takes search query from the form on the items page.
    Then queries the database for all items that match the search query and then renders the html page.
    :return: HTML page
    """
    query = request.form['search_bar']
    items = get_items(query)
    return render_template('items.html', products=items)


@store.route('/item')
def item():
    """
    Displays a single item. Takes item id from the url and queries the database for the item.
    If user is logged in, it queries the database to check if the item is in their cart.
    Then renders the html page.
    :return: HTML page
    """
    item_id = request.args.get('item_id')
    product = get_single_item(item_id)
    user_id = current_user.id if current_user.is_authenticated else None
    return render_template('item.html', product=product,
                           already_in_cart=None if user_id is None else already_in_cart(item_id, user_id))


@store.route('/sold_items')
@login_required
def sold_items():
    """
    Displays all items sold by the current user. Takes current user's id from the session and queries
    the database for items sold by the user. Then renders the html page.
    :return: HTML page
    """
    user_id = current_user.id
    products = get_items_sold_by(user_id)
    return render_template('seller.html', products=products)


@store.route('/remove_from_cart')
@login_required
def remove_from_cart():
    """
    Handles POST request from the cart page. It takes item id from the form on the cart page and
    user id from the session. Then queries the database to remove the item from the user's cart.
    Flashes the message and redirects back to the cart page.
    :return: redirect response
    """
    item_id = request.args.get('item_id')
    user_id = current_user.id
    dao_remove_from_cart(user_id, item_id)
    flash('Item has been removed from cart')
    return redirect(url_for('store.cart'))


@store.route('/change_cart_quantity', methods=['POST'])
@login_required
def change_cart_quantity():
    """
    Handles POST request from the cart page. It takes item id from the form on the cart page and
    user id from the session. Then queries the database to change the quantity of the item in the
    user's cart. Flashes the message and redirects back to the cart page.
    :return: redirect response
    """
    item_id = request.args.get('item_id')
    user_id = current_user.id
    new_quantity = request.form['quantity']
    change_quantity_in_cart(new_quantity, item_id, user_id)
    flash('Quantity has been updated')
    return redirect(url_for('store.cart'))


@store.route('/buy')
@login_required
def buy():
    """
    Handles request from the cart page. It takes user id from the session and queries the database
    to get all items in the user's cart. Then renders the html page to confirm the order.
    :return: HTML page
    """
    user_id = current_user.id
    cart_items = get_user_cart(user_id)
    total_price = sum(i['ItemPrice'] * i['CartItemQuantity'] for i in cart_items)
    return render_template('buy.html', total_price=total_price, products=cart_items)


@store.route('/confirm_purchase')
@login_required
def confirm_purchase():
    """
    Handles request from the buy page. It takes user id from the session and queries the database
    to get all items in the user's cart. Then creates a purchase in the database and then adds
    all items in the user's cart to the purchase. Then removes all items from the user's cart.
    Flashes the message and redirects to user's cart.
    :return: redirect response
    """
    user_id = current_user.id
    cart_items = get_user_cart(user_id)
    purchase_id = create_purchase(user_id)
    for i in cart_items:
        add_item_to_purchase(purchase_id, i['ItemId'], i['CartItemQuantity'], i['ItemPrice'])
        set_current_availability(i['ItemAvailability'] - i['CartItemQuantity'], i['ItemId'])
        dao_remove_from_cart(user_id, i['ItemId'])
    flash('Purchase confirmed!')
    return redirect(url_for('store.cart'))


@store.route('/add_to_cart', methods=['POST'])
@login_required
def add_to_cart():
    """
    Handles POST request from the item page. It takes item id from the form on the item page and
    user id from the session. Then queries the database to add the item to the user's cart.
    Flashes the message and redirects back to the item page.
    :return: redirect response
    """
    user_id = current_user.id
    item_id = request.args.get('item_id')
    quantity = request.form['quantity']
    dao_add_to_cart(user_id, item_id, quantity)
    flash('Item added to cart.')
    return redirect(url_for('store.item', item_id=item_id))


@store.route('/change_price', methods=['POST'])
@login_required
def change_price():
    """
    Handles POST request from the seller's item page. It takes item id from the form on the item page and
    user id from the session. Then queries the database to change the price of the item.
    Flashes the message and redirects back to the item page.
    :return: redirect response
    """
    item_id = request.args.get('item_id')
    new_price = request.form['new_price']
    update_item_price(new_price, item_id)
    flash('Price updated.')
    return redirect(url_for('store.sold_items'))


@store.route('/change_availability', methods=['POST'])
@login_required
def change_availability():
    """
    Handles POST request from the seller's item page. It takes item id from the form on the item page and
    user id from the session. Then queries the database to change the availability of the item.
    Flashes the message and redirects back to the item page.
    :return: redirect response
    """
    item_id = request.args.get('item_id')
    new_availability = request.form['new_availability']
    set_current_availability(new_availability, item_id)
    flash('Availability updated.')
    return redirect(url_for('store.sold_items'))


@store.route('/add_item')
@login_required
def add_item():
    """
    Handles request from the seller's page. It renders the html page to add a new item.
    :return: HTML page
    """
    return render_template('add_item.html')


@store.route('/add_item', methods=['POST'])
@login_required
def add_item_post():
    """
    Handles POST request from the seller's page. It takes item name, description, price, availability
    from the form on the seller's page and user id from the session. Then queries the database to add
    the item to the database. Flashes the message and redirects back to the seller's page.
    :return:
    """
    user_id = current_user.id
    name = request.form['productName']
    description = request.form['productDescription']
    price = request.form['productPrice']
    availability = request.form['productAvailability']
    unit = request.form['productUnit']
    add_product(price, name, description, availability, unit, user_id)
    flash('Product added.')
    return redirect(url_for('store.sold_items'))


@login_required
@store.route('/delete_item')
def delete_item():
    """
    Handles request from the seller's page. It takes item id from the form on the seller's page and
    queries the database to delete the item. Flashes the message and redirects back to the seller's page.
    :return: redirect response
    """
    item_id = request.args.get('item_id')
    dao_delete_item(item_id)
    flash('Product deleted.')
    return redirect(url_for('store.sold_items'))


@login_required
@store.route('/profile')
def profile():
    """
    Handles request from the navbar. For sellers, it queries the database for the seller report, calculates
    the total value of all items sold, and renders the html page. For customer, it queries the database for
    the customer report, calculates the total value of all items ordered in every order,
    and renders the html page. For other users, it redirects to main page.
    :return: HTML page
    """
    if current_user.usertype == 'seller':
        products = get_seller_report(current_user.id)
        total = sum(i['PurchasedItemPrice'] * i['PurchasedItemsQuantity'] for i in products)
        return render_template('seller_profile.html', products=products, name=current_user.name, total=total)
    elif current_user.usertype == 'customer':
        products = get_purchased_items(current_user.id)
        groups = groupby(products, projection=lambda p: p['PurchaseId'])
        id_to_date_map = {p['PurchaseId']: p['PurchaseDate'] for p in products}
        return render_template('customer_profile.html', groups=groups, name=current_user.name,
                               id_to_date_map=id_to_date_map)
    return redirect(url_for('main.index'))
