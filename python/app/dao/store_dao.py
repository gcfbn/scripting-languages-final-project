from time import sleep

import pymysql.cursors
from .sql_scripts import *

SQL_USER = 'flask'
SQL_PASSWORD = 'flask'
SQL_HOST = 'db'
SQL_DATABASE = 'store'

conn = None
conn_ok = False

while not conn_ok:
    try:
        conn = pymysql.connect(user=SQL_USER, passwd=SQL_PASSWORD, host=SQL_HOST, database=SQL_DATABASE)
    except:
        sleep(0.5)
        continue
    conn_ok = True

cursor = conn.cursor(pymysql.cursors.DictCursor)


def get_user_cart(user_id):
    cursor.execute(get_user_cart_query, (user_id,))
    return cursor.fetchall()


def get_user_purchases(user_id):
    cursor.execute(get_user_purchases_query, (user_id,))
    return cursor.fetchall()


def get_purchased_items(purchase_id):
    cursor.execute(get_purchased_items_query, (purchase_id,))
    return cursor.fetchall()


def get_items(item_name=''):
    cursor.execute(get_items_query, (item_name,))
    return cursor.fetchall()


def add_product(item_price, item_name, item_descr, item_availability, item_unit, seller_id):
    cursor.execute(add_product_query, (item_price, item_name, item_descr, item_availability, item_unit, seller_id))
    conn.commit()
    return cursor.fetchall()


def add_to_cart(user_id, item_id, quantity):
    cursor.execute(add_to_cart_query, (user_id, item_id, quantity))
    conn.commit()
    return cursor.fetchall()


def remove_from_cart(user_id, item_id):
    cursor.execute(remove_from_cart_query, (user_id, item_id))
    conn.commit()
    return cursor.fetchall()


def change_quantity_in_cart(quantity, item_id, user_id):
    cursor.execute(change_quantity_in_cart_query, (quantity, item_id, user_id))
    conn.commit()
    return cursor.fetchall()


def create_purchase(user_id):
    cursor.execute(create_purchase_query, (user_id,))
    conn.commit()
    cursor.execute(get_last_item_id_query)
    return cursor.fetchone()['LAST_INSERT_ID()']


def add_item_to_purchase(purchase_id, item_id, quantity, price):
    cursor.execute(add_item_to_purchase_query, (purchase_id, item_id, quantity, price))
    conn.commit()
    return cursor.fetchall()


def set_current_availability(availability, item_id):
    cursor.execute(set_current_availability_query, (availability, item_id))
    conn.commit()
    return cursor.fetchall()


def get_items_sold_by(seller_id):
    cursor.execute(get_items_sold_by_query, (seller_id,))
    return cursor.fetchall()


def update_item_price(new_price, item_id):
    cursor.execute(update_item_price_query, (new_price, item_id))
    conn.commit()
    return cursor.fetchall()


def get_single_item(item_id):
    cursor.execute(get_single_item_query, (item_id,))
    return cursor.fetchone()


def already_in_cart(item_id, user_id):
    cursor.execute(already_in_cart_query, (item_id, user_id))
    result = cursor.fetchone()
    return not (result is None)


def delete_item(item_id):
    cursor.execute(delete_item_query, (item_id,))
    conn.commit()
    return cursor.fetchall()
