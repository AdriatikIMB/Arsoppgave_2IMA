CREATE DATABASE IF NOT EXISTS webshop;

USE webshop;

CREATE TABLE IF NOT EXISTS products (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    price DECIMAL(10,2) NOT NULL
);

-- Eksempler på produkter
INSERT INTO products (name, price) VALUES
('Produkt 1', 199.99),
('Produkt 2', 299.99),
('Produkt 3', 149.99);
