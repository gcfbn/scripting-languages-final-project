CREATE USER IF NOT EXISTS 'flask'@'%' IDENTIFIED WITH mysql_native_password BY 'flask';
GRANT ALL PRIVILEGES ON *.* TO 'flask'@'%';
FLUSH PRIVILEGES;