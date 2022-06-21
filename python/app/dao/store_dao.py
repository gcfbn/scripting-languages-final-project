from time import sleep

import pymysql.cursors
from .sql_scripts import *

# MYSQL database connection config
SQL_USER = 'flask'
SQL_PASSWORD = 'flask'
SQL_HOST = 'db'
SQL_DATABASE = 'store'

conn = None
conn_ok = False

# sometimes it takse few seconds for the database to start
# so it tries few times to connect to the database
while not conn_ok:
    try:
        conn = pymysql.connect(user=SQL_USER, passwd=SQL_PASSWORD, host=SQL_HOST, database=SQL_DATABASE)
    except:
        sleep(0.5)
        continue
    conn_ok = True

cursor = conn.cursor(pymysql.cursors.DictCursor)


def get_user_cart(user_id):
    """
    Returns a list of items in the cart of the user with the given id
    :param user_id: Cart's owner's id
    :return: Tuple of items in the cart
    """
    cursor.execute(get_user_cart_query, (user_id,))
    return cursor.fetchall()


def get_user_purchases(user_id):
    """
    Returns a list of purchases made by the user with the given id
    :param user_id: Id of user that made the purchases
    :return: Tuple of purchases made by the user
    """
    cursor.execute(get_user_purchases_query, (user_id,))
    return cursor.fetchall()


def get_purchased_items(user_id):
    """
    Returns a list of all the items purchased by the user with the given id.
    :param user_id: Id of user that made the purchases
    :return: Tuple of purchased items
    """
    cursor.execute(get_purchased_items_query, (user_id,))
    return cursor.fetchall()


def get_items(item_name=''):
    """
    Returns a list of items with the given name. If no name is given, returns all items.
    :param item_name: Search query
    :return: Tuple of items
    """
    cursor.execute(get_items_query, (item_name,))
    return cursor.fetchall()


def add_product(item_price, item_name, item_descr, item_availability, item_unit, seller_id):
    """
    Adds a new item to the database
    :param item_price: Item unit price
    :param item_name: Item name
    :param item_descr: Item description
    :param item_availability: Number of items in stock
    :param item_unit: Item unit, e.g. "kg", "pcs"
    :param seller_id: Id of the user that sells the item
    :return: Tuple returned by the database
    """
    cursor.execute(add_product_query, (item_price, item_name, item_descr, item_availability, item_unit, seller_id))
    conn.commit()
    return cursor.fetchall()


def add_to_cart(user_id, item_id, quantity):
    """
    Adds an item to the cart of the user with the given id
    :param user_id: Cart's owner
    :param item_id: Item to be added to the cart
    :param quantity: Quantity of the item to be added to the cart
    :return: Tuple returned by the database
    """
    cursor.execute(add_to_cart_query, (user_id, item_id, quantity))
    conn.commit()
    return cursor.fetchall()


def remove_from_cart(user_id, item_id):
    """
    Removes an item from the cart of the user with the given id
    :param user_id: Cart's owner
    :param item_id: Item to be removed
    :return: Tuple returned by the database
    """
    cursor.execute(remove_from_cart_query, (user_id, item_id))
    conn.commit()
    return cursor.fetchall()


def change_quantity_in_cart(quantity, item_id, user_id):
    """
    Changes the quantity of an item in the cart of the user with the given id
    :param quantity: New quantity of the item
    :param item_id: Item to be changed
    :param user_id: Cart's owner
    :return: Tuple returned by the database
    """
    cursor.execute(change_quantity_in_cart_query, (quantity, item_id, user_id))
    conn.commit()
    return cursor.fetchall()


def create_purchase(user_id):
    """
    Creates a new purchase for the user with the given id
    :param user_id: User that made the purchase
    :return: Id of the new purchase
    """
    cursor.execute(create_purchase_query, (user_id,))
    conn.commit()
    cursor.execute(get_last_item_id_query)
    return cursor.fetchone()['LAST_INSERT_ID()']


def add_item_to_purchase(purchase_id, item_id, quantity, price):
    """
    Adds an item to the purchase with the given id
    :param purchase_id: Purchase
    :param item_id: Item to be added
    :param quantity: Quantity of the item to be added
    :param price: Price of the item to be added
    :return: Tuple returned by the database
    """
    cursor.execute(add_item_to_purchase_query, (purchase_id, item_id, quantity, price))
    conn.commit()
    return cursor.fetchall()


def set_current_availability(availability, item_id):
    """
    Sets the current availability of the item with the given id
    :param availability: New availability of the item
    :param item_id: Item to be changed
    :return: Tuple returned by the database
    """
    cursor.execute(set_current_availability_query, (availability, item_id))
    conn.commit()
    return cursor.fetchall()


def get_items_sold_by(seller_id):
    """
    Returns a list of items being sold the user with the given id
    :param seller_id: Seller's id
    :return: Tuple of items being sold by the user
    """
    cursor.execute(get_items_sold_by_query, (seller_id,))
    return cursor.fetchall()


def update_item_price(new_price, item_id):
    """
    Updates the price of the item with the given id
    :param new_price: New price of the item
    :param item_id: Item to be changed
    :return: Tuple returned by the database
    """
    cursor.execute(update_item_price_query, (new_price, item_id))
    conn.commit()
    return cursor.fetchall()


def get_single_item(item_id):
    """
    Returns a single item with the given id
    :param item_id: Item's id
    :return: Dictionary with the item's data
    """
    cursor.execute(get_single_item_query, (item_id,))
    return cursor.fetchone()


def already_in_cart(item_id, user_id):
    """
    Checks if the item with the given id is already in the cart of the user with the given id
    :param item_id: Item's id
    :param user_id: Cart's owner
    :return: True if the item is in the cart, False otherwise
    """
    cursor.execute(already_in_cart_query, (item_id, user_id))
    result = cursor.fetchone()
    return not (result is None)


def delete_item(item_id):
    """
    Deletes the item with the given id
    :param item_id: Item's id
    :return: Tuple returned by the database
    """
    cursor.execute(delete_item_query, (item_id,))
    conn.commit()
    return cursor.fetchall()


def get_seller_report(user_id):
    """
    Returns a list of all items sold by the user with the given id
    :param user_id: Seller's id
    :return: Tuple of the items sold by the user
    """
    cursor.execute(get_seller_report_query, (user_id,))
    return cursor.fetchall()
