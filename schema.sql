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
(1, 1, 'Organic Royal Gala Apple', 180.00, 'kg', '2026-07-20', '2026-08-05', 50, 10.00, '2026-07-01', 'Mandya Organic Orchards'),
(2, 1, 'Organic Robusta Banana', 60.00, 'kg', '2026-07-22', '2026-07-30', 80, 8.00, '2026-07-01', 'Maddur Riverbank Orchards'),
(3, 1, 'Organic Alphonso Mango', 350.00, 'kg', '2026-07-15', '2026-07-28', 40, 12.00, '2026-07-01', 'Ratnagiri Heritage Mango Groves'),
(4, 1, 'Organic Nagpur Orange', 90.00, 'kg', '2026-07-18', '2026-08-08', 60, 10.00, '2026-07-01', 'Nagpur Citrus Growers Co-op'),
(5, 1, 'Organic Red Pomegranate', 220.00, 'kg', '2026-07-19', '2026-08-15', 45, 12.00, '2026-07-01', 'Solapur Organic Farms'),
(6, 1, 'Organic Pink Guava', 80.00, 'kg', '2026-07-21', '2026-08-01', 55, 6.00, '2026-07-01', 'Kolar Fruit Growers'),
(7, 1, 'Organic Hybrid Watermelon', 40.00, 'kg', '2026-07-24', '2026-08-10', 70, 10.00, '2026-07-01', 'Challakere Riverbed Farms'),
(8, 1, 'Organic Pink Dragon Fruit', 250.00, 'kg', '2026-07-23', '2026-08-07', 30, 14.00, '2026-07-01', 'Deccan Exotic Fruit Farms'),
(9, 1, 'Organic Queen Pineapple', 110.00, 'kg', '2026-07-17', '2026-08-07', 40, 8.00, '2026-07-01', 'Shivamogga Foothill Orchards'),
(10, 1, 'Organic Sweet Lime (Mosambi)', 95.00, 'kg', '2026-07-20', '2026-08-10', 50, 9.00, '2026-07-01', 'Anantapur Fruit Orchards'),
(11, 2, 'Organic Country Tomato', 45.00, 'kg', '2026-07-25', '2026-08-05', 100, 10.00, '2026-07-01', 'Maddur Riverbank Farms'),
(12, 2, 'Organic Fresh Potato', 35.00, 'kg', '2026-07-20', '2026-08-20', 120, 12.00, '2026-07-01', 'Hassan Organic Potato Growers'),
(13, 2, 'Organic Red Onion', 40.00, 'kg', '2026-07-18', '2026-08-30', 150, 11.00, '2026-07-01', 'Chitradurga Farm Collective'),
(14, 2, 'Organic Farm Carrot', 60.00, 'kg', '2026-07-24', '2026-08-10', 90, 14.00, '2026-07-01', 'Ooty Hill Organic Orchards'),
(15, 2, 'Organic Green Cabbage', 30.00, 'kg', '2026-07-26', '2026-08-08', 80, 14.00, '2026-07-01', 'Kolar Veg Growers'),
(16, 2, 'Organic Fresh Cauliflower', 50.00, 'kg', '2026-07-25', '2026-08-03', 70, 9.00, '2026-07-01', 'Belagavi Farm Co-Op'),
(17, 2, 'Organic Green Capsicum', 80.00, 'kg', '2026-07-23', '2026-08-04', 65, 11.00, '2026-07-01', 'Mandya Polyhouse Organic Farms'),
(18, 2, 'Organic Purple Brinjal', 40.00, 'kg', '2026-07-22', '2026-08-02', 75, 11.00, '2026-07-01', 'Tumakuru Farm Collective'),
(19, 2, 'Organic Ruby Beetroot', 50.00, 'kg', '2026-07-21', '2026-08-15', 85, 9.00, '2026-07-01', 'Chikkaballapur Organic Belt'),
(20, 2, 'Organic Sweet Corn', 45.00, 'kg', '2026-07-24', '2026-08-06', 110, 10.00, '2026-07-01', 'Davanagere Grain & Produce Co-op'),
(21, 3, 'Organic Whole Grains', 150.00, 'kg', '2026-07-10', '2027-07-10', 200, 0.00, '2026-07-01', 'Mysuru Heritage Paddy Farms'),
(22, 4, 'Organic Native Pulses', 180.00, 'kg', '2026-07-12', '2027-01-12', 150, 10.00, '2026-07-01', 'Kalaburagi Pulse Collective'),
(23, 5, 'Organic Pure A2 Milk', 95.00, 'L', '2026-07-28', '2026-07-31', 40, 0.00, '2026-07-01', 'Pandavapura Bilona Dairy'),
(24, 6, 'Organic Aromatic Spices', 210.00, 'g', '2026-07-05', '2027-07-05', 80, 8.00, '2026-07-01', 'Sirsi Spice Hills Garden'),
(25, 7, 'Organic Herbal Beverage', 135.00, 'L', '2026-07-18', '2026-10-18', 60, 0.00, '2026-07-01', 'Chikmagalur Herbal Valley'),
(26, 8, 'Organic Premium Almonds', 450.00, 'g', '2026-07-08', '2027-07-08', 90, 10.00, '2026-07-01', 'Kolar Organic Nut Growers'),
(27, 9, 'Organic Ancient Foxtail Millet', 160.00, 'kg', '2026-07-14', '2027-01-14', 120, 0.00, '2026-07-01', 'Nagamangala Rainfed Farms'),
(28, 10, 'Organic Cold Pressed Mustard Oil', 320.00, 'L', '2026-07-22', '2027-07-22', 75, 8.00, '2026-07-01', 'Challakere Wooden Ghani Mill');

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

