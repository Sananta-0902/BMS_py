-- billing_system.sql

CREATE DATABASE IF NOT EXISTS billing;
USE billing;

-- Users table
drop table users;
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(100) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    role VARCHAR(6) NOT NULL
);

-- Products table
CREATE TABLE IF NOT EXISTS products (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    price DECIMAL(10, 2) NOT NULL
);

-- Invoices table
CREATE TABLE IF NOT EXISTS invoices (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    date DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

-- Invoice items table
CREATE TABLE IF NOT EXISTS invoice_items (
    id INT AUTO_INCREMENT PRIMARY KEY,
    invoice_id INT NOT NULL,
    product_id INT NOT NULL,
    quantity INT NOT NULL,
    FOREIGN KEY (invoice_id) REFERENCES invoices(id) ON DELETE CASCADE,
    FOREIGN KEY (product_id) REFERENCES products(id)
);

-- Sample Admin User (password: admin123)
INSERT INTO user (username, password, role)
VALUES ('admin', '$pbkdf2-sha256$29000$DY4RffL6WZKoQvlRkT3jMw$gdroG3iRxFV1Kf7eWHDyHR2d7nExFzPMzmGkSfGAkPY', 'admin')
ON DUPLICATE KEY UPDATE username=username;

-- Sample User (password: user123)
INSERT INTO users (username, password, role)
VALUES ('user', '$pbkdf2-sha256$29000$03RhqW7Z4go5AwS06pIvqQ$F5bBYy5QUddoZQRoJVprkL9X2EuTGAdFwTfaaEKOfy4', 'user')
ON DUPLICATE KEY UPDATE username=username;

insert into products(id,name, price)
values ('1', "notebook", "50");

ALTER TABLE users ADD COLUMN role VARCHAR(20) NOT NULL DEFAULT 'user';

drop table users;
update users set enum= "varchar(6)";
ALTER TABLE users MODIFY COLUMN role VARCHAR(20) NOT NULL;
ALTER TABLE products CHANGE id product_id INT NOT NULL AUTO_INCREMENT;
alter table products change product_id id int not null auto_increment;
