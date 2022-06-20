CREATE DATABASE IF NOT EXISTS store;
USE store;

CREATE USER IF NOT EXISTS 'flask'@'%' IDENTIFIED WITH mysql_native_password BY 'flask';
GRANT ALL PRIVILEGES ON *.* TO 'flask'@'%';
FLUSH PRIVILEGES;

CREATE TABLE IF NOT EXISTS Items
(
    ItemId           int         NOT NULL AUTO_INCREMENT,
    ItemPrice        float(9, 2) NOT NULL,
    ItemName         varchar(63) NOT NULL,
    ItemDescr        text,
    ItemAvailability int         NOT NULL,
    ItemUnit         varchar(15) NOT NULL,
    SellerId         int         NOT NULL,
    IsDeleted        boolean,
    PRIMARY KEY (ItemId)
);

CREATE TABLE IF NOT EXISTS Carts
(
    UserId           int NOT NULL,
    ItemId           int NOT NULL,
    CartItemQuantity int NOT NULL,
    PRIMARY KEY (UserId, ItemId),
    FOREIGN KEY (ItemId) REFERENCES Items (ItemId)
);

CREATE TABLE IF NOT EXISTS Purchases
(
    PurchaseId   int  NOT NULL AUTO_INCREMENT,
    UserId       int  NOT NULL,
    PurchaseDate date NOT NULL,
    PRIMARY KEY (PurchaseId)
);

CREATE TABLE IF NOT EXISTS Purchased_Items
(
    PurchaseId             int NOT NULL,
    ItemId                 int NOT NULL,
    PurchasedItemsQuantity int NOT NULL,
    PurchasedItemPrice     float(9, 2) NOT NULL,
    PRIMARY KEY (PurchaseId, ItemId),
    FOREIGN KEY (PurchaseId) REFERENCES Purchases (PurchaseId),
    FOREIGN KEY (ItemId) REFERENCES Items (ItemId)
);