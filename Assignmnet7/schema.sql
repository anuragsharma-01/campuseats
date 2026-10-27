CREATE DATABASE IF NOT EXISTS campuseats;
USE campuseats;

DROP TABLE IF EXISTS dishes;

CREATE TABLE dishes (
  id INT PRIMARY KEY AUTO_INCREMENT,
  name VARCHAR(100) NOT NULL,
  price DECIMAL(10,2) NOT NULL,
  available BOOLEAN NOT NULL DEFAULT TRUE
);

INSERT INTO dishes (name, price, available) VALUES
('Paneer Tikka Sandwich', 80.00, TRUE),
('Veg Biryani', 120.00, TRUE),
('Masala Dosa', 70.00, TRUE),
('Cold Coffee', 60.00, FALSE);
