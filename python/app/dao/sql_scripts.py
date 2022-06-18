get_user_cart_query = """SELECT Items.ItemId, Items.ItemPrice, Items.ItemName, Items.ItemUnit, Items.ItemAvailability, Carts.CartItemQuantity
FROM Carts INNER JOIN Items ON Carts.ItemId=Items.ItemId
WHERE Carts.UserId = %s;"""

get_user_purchases_query = """SELECT PurchaseId, PurchaseDate 
FROM Purchases
WHERE UserId = %s;"""

get_purchased_items_query = """SELECT PI.ItemId, I.ItemName, PI.PurchasedItemsQuantity, I.ItemUnit
FROM Purchases P INNER JOIN Purchased_Items PI on P.PurchaseId = PI.PurchaseId
INNER JOIN Items I on PI.ItemId = I.ItemId
WHERE P.PurchaseId = %s;"""

get_items_query = """SELECT ItemId, ItemName, ItemDescr, ItemPrice, ItemAvailability, ItemUnit
FROM Items
WHERE Items.ItemName LIKE CONCAT('%%', %s, '%%');"""

add_product_query = """INSERT INTO Items(ItemPrice, ItemName, ItemDescr, ItemAvailability, ItemUnit, SellerId)
    VALUE (%s, %s, %s, %s, %s, %s);"""

add_to_cart_query = """INSERT INTO Carts(UserId, ItemId, CartItemQuantity) 
    VALUE(%s, %s, %s);"""

remove_from_cart_query = """DELETE FROM Carts 
WHERE UserId = %s AND ItemId = %s"""

change_quantity_in_cart_query = """UPDATE Carts
SET CartItemQuantity = %s
WHERE ItemId = %s AND UserId = %s;"""

create_purchase_query = """INSERT INTO Purchases(UserId, PurchaseDate)
VALUE (%s, CURDATE());"""

add_item_to_purchase_query = """INSERT INTO Purchased_Items(PurchaseId, ItemId, PurchasedItemsQuantity)
VALUE(%s, %s, %s);"""

set_current_availability_query = """UPDATE Items
SET ItemAvailability = %s
WHERE ItemId = %s;"""

get_items_sold_by_query = """SELECT I.ItemId, I.ItemName, I.ItemPrice, I.ItemUnit, I.ItemAvailability,
SUM(PI.PurchasedItemsQuantity) AS NumberOfSoldItems 
FROM Items I LEFT JOIN Purchased_Items PI on I.ItemId = PI.ItemId
WHERE I.SellerId = %s;"""

update_item_price_query = """UPDATE Items
SET ItemPrice = %s
WHERE ItemId = %s;"""

get_last_item_id_query = """SELECT LAST_INSERT_ID() FROM Purchases;"""

get_single_item_query = """SELECT * FROM Items I WHERE I.ItemId = %s;"""

already_in_cart_query = """SELECT * FROM Carts C WHERE C.ItemId = %s AND C.UserId = %s;"""
