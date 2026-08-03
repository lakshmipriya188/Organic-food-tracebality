-- Organic Food Traceability Database Schema for MySQL

CREATE TABLE IF NOT EXISTS Category(
    category_id INT PRIMARY KEY AUTO_INCREMENT,
    category_name VARCHAR(100) NOT NULL,
    description TEXT
);

CREATE TABLE IF NOT EXISTS Product(
    product_id INT PRIMARY KEY AUTO_INCREMENT,
    category_id INT,
    product_name VARCHAR(100),
    price DECIMAL(10,2),
    unit VARCHAR(50) DEFAULT 'kg',
    manufacture_date DATE,
    expiry_date DATE,
    quantity INT,
    discount DECIMAL(5,2),
    onboarding_date DATE,
    manufacturer_name VARCHAR(100),
    FOREIGN KEY(category_id)
    REFERENCES Category(category_id)
);

-- Seed Default Categories
INSERT IGNORE INTO Category(category_id, category_name, description) VALUES
(1, 'Fruits', '100% Organic Farm-Fresh Fruits'),
(2, 'Vegetables', 'Fresh Organic Farm Vegetables'),
(3, 'Grains', 'Unpolished Traditional Whole Grains'),
(4, 'Pulses', 'Sun-dried Native Organic Pulses'),
(5, 'Dairy', 'Pure A2 Desi Cow Dairy Products'),
(6, 'Spices', 'Organic Aromatic Whole Spices'),
(7, 'Beverages', 'Natural Organic Drinks & Juices'),
(8, 'Dry Fruits', 'Premium Raw Organic Dry Fruits'),
(9, 'Millets', 'Nutrient-rich Ancient Organic Millets'),
(10, 'Oils', 'Traditional Wooden Cold-Pressed Oils');

-- Seed Default Products matching category_id with category-specific units
INSERT IGNORE INTO Product(product_id, category_id, product_name, price, unit, manufacture_date, expiry_date, quantity, discount, onboarding_date, manufacturer_name) VALUES
(1, 1, 'Organic Fresh Fruits', 120.00, 'kg', '2026-07-20', '2026-08-05', 50, 14.00, '2026-07-01', 'Mandya Organic Fruit Orchards'),
(2, 2, 'Organic Farm Vegetables', 85.00, 'kg', '2026-07-25', '2026-08-02', 100, 10.00, '2026-07-01', 'Maddur Riverbank Farms'),
(3, 3, 'Organic Whole Grains', 150.00, 'kg', '2026-07-10', '2027-07-10', 200, 0.00, '2026-07-01', 'Mysuru Heritage Paddy Farms'),
(4, 4, 'Organic Native Pulses', 180.00, 'kg', '2026-07-12', '2027-01-12', 150, 10.00, '2026-07-01', 'Kalaburagi Pulse Collective'),
(5, 5, 'Organic Pure A2 Milk', 95.00, 'L', '2026-07-28', '2026-07-31', 40, 0.00, '2026-07-01', 'Pandavapura Bilona Dairy'),
(6, 6, 'Organic Aromatic Spices', 210.00, '250g', '2026-07-05', '2027-07-05', 80, 8.00, '2026-07-01', 'Sirsi Spice Hills Garden'),
(7, 7, 'Organic Herbal Beverage', 135.00, '1L bottle', '2026-07-18', '2026-10-18', 60, 0.00, '2026-07-01', 'Chikmagalur Herbal Valley'),
(8, 8, 'Organic Premium Almonds', 450.00, '500g', '2026-07-08', '2027-07-08', 90, 10.00, '2026-07-01', 'Kolar Organic Nut Growers'),
(9, 9, 'Organic Ancient Foxtail Millet', 160.00, 'kg', '2026-07-14', '2027-01-14', 120, 0.00, '2026-07-01', 'Nagamangala Rainfed Farms'),
(10, 10, 'Organic Cold Pressed Mustard Oil', 320.00, '1L', '2026-07-22', '2027-07-22', 75, 8.00, '2026-07-01', 'Challakere Wooden Ghani Mill');

-- Customer Details Table
CREATE TABLE IF NOT EXISTS Customer_Details (
    customer_id INT AUTO_INCREMENT PRIMARY KEY,
    customer_name VARCHAR(100) NOT NULL,
    email_id VARCHAR(100) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL
);

-- Seed Initial Customer Details
INSERT IGNORE INTO Customer_Details (customer_name, email_id, password)
VALUES
('Rahul Sharma', 'rahul@gmail.com', 'Rahul@123'),
('Priya Singh', 'priya@gmail.com', 'Priya@123'),
('Amit Kumar', 'amit@gmail.com', 'Amit@123'),
('Sneha Reddy', 'sneha@gmail.com', 'Sneha@123'),
('Arjun Patel', 'arjun@gmail.com', 'Arjun@123');

-- Cart Table
CREATE TABLE IF NOT EXISTS Cart (
    cart_id INT AUTO_INCREMENT PRIMARY KEY,
    customer_id INT NOT NULL,
    product_id INT NOT NULL,
    product_count INT NOT NULL,
    product_price DECIMAL(10,2) NOT NULL,
    product_discount DECIMAL(5,2) NOT NULL,
    price_after_discount DECIMAL(10,2) NOT NULL,

    CONSTRAINT fk_cart_customer
        FOREIGN KEY (customer_id)
        REFERENCES Customer_Details(customer_id),

    CONSTRAINT fk_cart_product
        FOREIGN KEY (product_id)
        REFERENCES Product(product_id)
);

-- Order Details Table
CREATE TABLE IF NOT EXISTS Order_Details (
    order_id INT AUTO_INCREMENT PRIMARY KEY,
    customer_id INT NOT NULL,
    product_id INT NOT NULL,
    product_count INT NOT NULL,
    product_price DECIMAL(10,2) NOT NULL,
    product_discount DECIMAL(5,2) NOT NULL,
    price_after_discount DECIMAL(10,2) NOT NULL,
    order_date DATE NOT NULL,
    order_time TIME NOT NULL,

    CONSTRAINT fk_order_customer
        FOREIGN KEY (customer_id)
        REFERENCES Customer_Details(customer_id),

    CONSTRAINT fk_order_product
        FOREIGN KEY (product_id)
        REFERENCES Product(product_id)
);

