-- CampusEats Assignment 2
-- Database schema sketch.
-- Service boundaries are preserved: each service owns only its own tables.
-- Cross-service IDs are application-level references, not cross-service foreign keys.

CREATE DATABASE IF NOT EXISTS campuseats;
USE campuseats;

-- =========================================================
-- Identity & Administration Service
-- =========================================================
CREATE TABLE users (
    user_id BIGINT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(120) NOT NULL,
    email VARCHAR(180) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    role ENUM('STUDENT','FOOD_PROVIDER','ADMIN') NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE provider_profiles (
    provider_id BIGINT PRIMARY KEY AUTO_INCREMENT,
    user_id BIGINT NOT NULL,
    provider_name VARCHAR(150) NOT NULL,
    campus VARCHAR(120) NOT NULL,
    status ENUM('ACTIVE','INACTIVE') NOT NULL DEFAULT 'ACTIVE',
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);

-- =========================================================
-- Catalogue Service
-- =========================================================
CREATE TABLE restaurants (
    restaurant_id BIGINT PRIMARY KEY AUTO_INCREMENT,
    provider_id BIGINT NOT NULL, -- external reference owned by Identity service
    name VARCHAR(150) NOT NULL,
    campus VARCHAR(120) NOT NULL,
    status ENUM('OPEN','CLOSED') NOT NULL DEFAULT 'OPEN'
);

CREATE TABLE categories (
    category_id BIGINT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL UNIQUE
);

CREATE TABLE menus (
    menu_id BIGINT PRIMARY KEY AUTO_INCREMENT,
    restaurant_id BIGINT NOT NULL,
    name VARCHAR(150) NOT NULL,
    status ENUM('ACTIVE','INACTIVE') NOT NULL DEFAULT 'ACTIVE',
    FOREIGN KEY (restaurant_id) REFERENCES restaurants(restaurant_id)
);

CREATE TABLE food_items (
    item_id BIGINT PRIMARY KEY AUTO_INCREMENT,
    menu_id BIGINT NOT NULL,
    category_id BIGINT NOT NULL,
    name VARCHAR(150) NOT NULL,
    description TEXT,
    price DECIMAL(10,2) NOT NULL,
    available BOOLEAN NOT NULL DEFAULT TRUE,
    FOREIGN KEY (menu_id) REFERENCES menus(menu_id),
    FOREIGN KEY (category_id) REFERENCES categories(category_id)
);

CREATE TABLE pickup_locations (
    pickup_location_id BIGINT PRIMARY KEY AUTO_INCREMENT,
    campus VARCHAR(120) NOT NULL,
    name VARCHAR(150) NOT NULL,
    address VARCHAR(255)
);

-- =========================================================
-- Order Service
-- =========================================================
CREATE TABLE orders (
    order_id BIGINT PRIMARY KEY AUTO_INCREMENT,
    student_id BIGINT NOT NULL, -- external reference owned by Identity service
    pickup_location_id BIGINT NOT NULL, -- external reference owned by Catalogue service
    status ENUM('PLACED','ACCEPTED','REJECTED','PREPARING','READY','COMPLETED','CANCELLED') NOT NULL DEFAULT 'PLACED',
    total_amount DECIMAL(10,2) NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE order_items (
    order_item_id BIGINT PRIMARY KEY AUTO_INCREMENT,
    order_id BIGINT NOT NULL,
    item_id BIGINT NOT NULL, -- external reference owned by Catalogue service
    quantity INT NOT NULL,
    unit_price DECIMAL(10,2) NOT NULL,
    FOREIGN KEY (order_id) REFERENCES orders(order_id)
);

-- =========================================================
-- Payment Service
-- =========================================================
CREATE TABLE payments (
    payment_id BIGINT PRIMARY KEY AUTO_INCREMENT,
    order_id BIGINT NOT NULL, -- external reference owned by Order service
    amount DECIMAL(10,2) NOT NULL,
    method ENUM('CARD','UPI','WALLET','CASH') NOT NULL,
    status ENUM('PENDING','AUTHORIZED','DECLINED','REFUNDED') NOT NULL DEFAULT 'PENDING',
    transaction_reference VARCHAR(180),
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);
