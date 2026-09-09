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
    manufacture_date DATE,
    expiry_date DATE,
    quantity INT,
    discount DECIMAL(5,2),
    unit VARCHAR(50) DEFAULT 'kg',
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
INSERT IGNORE INTO Product(product_id, category_id, product_name, price, manufacture_date, expiry_date, quantity, discount, unit) VALUES
(1, 1, 'Organic Royal Gala Apple', 180.00, '2026-07-20', '2026-08-05', 50, 10.00, 'kg'),
(2, 1, 'Organic Robusta Banana', 60.00, '2026-07-22', '2026-07-30', 80, 8.00, 'kg'),
(3, 1, 'Organic Alphonso Mango', 350.00, '2026-07-15', '2026-07-28', 40, 12.00, 'kg'),
(4, 1, 'Organic Nagpur Orange', 90.00, '2026-07-18', '2026-08-08', 60, 10.00, 'kg'),
(5, 1, 'Organic Red Pomegranate', 220.00, '2026-07-19', '2026-08-15', 45, 12.00, 'kg'),
(6, 1, 'Organic Pink Guava', 80.00, '2026-07-21', '2026-08-01', 55, 6.00, 'kg'),
(7, 1, 'Organic Hybrid Watermelon', 40.00, '2026-07-24', '2026-08-10', 70, 10.00, 'kg'),
(8, 1, 'Organic Pink Dragon Fruit', 250.00, '2026-07-23', '2026-08-07', 30, 14.00, 'kg'),
(9, 1, 'Organic Queen Pineapple', 110.00, '2026-07-17', '2026-08-07', 40, 8.00, 'kg'),
(10, 1, 'Organic Sweet Lime (Mosambi)', 95.00, '2026-07-20', '2026-08-10', 50, 9.00, 'kg'),
(11, 2, 'Organic Country Tomato', 45.00, '2026-07-25', '2026-08-05', 100, 10.00, 'kg'),
(12, 2, 'Organic Fresh Potato', 35.00, '2026-07-20', '2026-08-20', 120, 12.00, 'kg'),
(13, 2, 'Organic Red Onion', 40.00, '2026-07-18', '2026-08-30', 150, 11.00, 'kg'),
(14, 2, 'Organic Farm Carrot', 60.00, '2026-07-24', '2026-08-10', 90, 14.00, 'kg'),
(15, 2, 'Organic Green Cabbage', 30.00, '2026-07-26', '2026-08-08', 80, 14.00, 'kg'),
(16, 2, 'Organic Fresh Cauliflower', 50.00, '2026-07-25', '2026-08-03', 70, 9.00, 'kg'),
(17, 2, 'Organic Green Capsicum', 80.00, '2026-07-23', '2026-08-04', 65, 11.00, 'kg'),
(18, 2, 'Organic Purple Brinjal', 40.00, '2026-07-22', '2026-08-02', 75, 11.00, 'kg'),
(19, 2, 'Organic Ruby Beetroot', 50.00, '2026-07-21', '2026-08-15', 85, 9.00, 'kg'),
(20, 2, 'Organic Sweet Corn', 45.00, '2026-07-24', '2026-08-06', 110, 10.00, 'kg'),
(21, 3, 'Organic Unpolished Brown Rice', 150.00, '2026-07-10', '2027-07-10', 200, 14.00, 'kg'),
(22, 3, 'Organic Khapli Whole Wheat', 85.00, '2026-07-12', '2027-07-12', 250, 10.00, 'kg'),
(23, 3, 'Organic Pearl Barley Grain', 110.00, '2026-07-14', '2027-07-14', 140, 12.00, 'kg'),
(24, 3, 'Organic Raw Buckwheat (Kuttu)', 160.00, '2026-07-16', '2027-07-16', 110, 11.00, 'kg'),
(25, 3, 'Organic White Quinoa Grain', 280.00, '2026-07-18', '2027-07-18', 90, 12.00, 'kg'),
(26, 3, 'Organic Whole Rolled Oats', 190.00, '2026-07-20', '2027-07-20', 130, 9.00, 'kg'),
(27, 3, 'Organic Whole Rye Grain', 140.00, '2026-07-22', '2027-07-22', 100, 10.00, 'kg'),
(28, 3, 'Organic Jowar Whole Grain', 95.00, '2026-07-15', '2027-07-15', 180, 9.00, 'kg'),
(29, 3, 'Organic Traditional Basmati Rice', 220.00, '2026-07-11', '2027-07-11', 160, 12.00, 'kg'),
(30, 3, 'Organic Kerala Red Matta Rice', 130.00, '2026-07-13', '2027-07-13', 150, 10.00, 'kg'),
(31, 4, 'Organic Unpolished Toor Dal (Arhar)', 180.00, '2026-07-12', '2027-01-12', 150, 10.00, 'kg'),
(32, 4, 'Organic Split Red Lentil (Masoor Dal)', 140.00, '2026-07-14', '2027-01-14', 160, 10.00, 'kg'),
(33, 4, 'Organic Kabuli Chickpeas (Chana)', 160.00, '2026-07-15', '2027-01-15', 140, 11.00, 'kg'),
(34, 4, 'Organic Whole Black Gram (Urad Whole)', 175.00, '2026-07-18', '2027-01-18', 130, 10.00, 'kg'),
(35, 4, 'Organic Whole Green Moong Dal', 155.00, '2026-07-16', '2027-01-16', 170, 9.00, 'kg'),
(36, 4, 'Organic Native Horse Gram (Kollu)', 120.00, '2026-07-13', '2027-01-13', 120, 11.00, 'kg'),
(37, 4, 'Organic Brown Cowpeas (Lobia)', 130.00, '2026-07-17', '2027-01-17', 110, 10.00, 'kg'),
(38, 4, 'Organic Kashmiri Rajma (Kidney Beans)', 195.00, '2026-07-19', '2027-01-19', 100, 11.00, 'kg'),
(39, 4, 'Organic Dried White Peas (Safed Matar)', 110.00, '2026-07-21', '2027-01-21', 125, 12.00, 'kg'),
(40, 4, 'Organic Native Yellow Soybeans', 135.00, '2026-07-20', '2027-01-20', 135, 10.00, 'kg'),
(41, 5, 'Organic Pure A2 Desi Cow Milk', 95.00, '2026-07-28', '2026-07-31', 100, 14.00, 'L'),
(42, 5, 'Organic Farm Fresh Buffalo Milk', 85.00, '2026-07-28', '2026-07-31', 120, 10.00, 'L'),
(43, 5, 'Organic Badam Flavoured Milk', 140.00, '2026-07-26', '2026-08-05', 80, 12.00, 'L'),
(44, 5, 'Organic Traditional Spiced Buttermilk (Chaas)', 60.00, '2026-07-27', '2026-08-02', 150, 14.00, 'L'),
(45, 5, 'Organic A2 Desi Cow Bilona Ghee', 1450.00, '2026-07-15', '2027-07-15', 60, 9.00, 'L'),
(46, 5, 'Organic Fresh Creamy Set Curd (Dahi)', 110.00, '2026-07-27', '2026-08-03', 90, 12.00, 'L'),
(47, 5, 'Organic Raw Almond Milk', 220.00, '2026-07-26', '2026-08-04', 70, 12.00, 'L'),
(48, 5, 'Organic Fresh Farm Malai Cream', 350.00, '2026-07-27', '2026-08-02', 50, 10.00, 'L'),
(49, 5, 'Organic Kesar Pista Flavoured Milk', 160.00, '2026-07-26', '2026-08-05', 75, 11.00, 'L'),
(50, 5, 'Organic Sweet Mango Lassi', 120.00, '2026-07-27', '2026-08-03', 85, 11.00, 'L'),
(51, 6, 'Organic Salem Whole Turmeric & Powder', 210.00, '2026-07-05', '2027-07-05', 80, 8.00, 'kg'),
(52, 6, 'Organic Guntur Red Chilli Powder', 280.00, '2026-07-08', '2027-07-08', 100, 10.00, 'kg'),
(53, 6, 'Organic Native Coriander Seeds (Dhania)', 160.00, '2026-07-10', '2027-07-10', 120, 11.00, 'kg'),
(54, 6, 'Organic Whole Cumin Seeds (Jeera)', 320.00, '2026-07-12', '2027-07-12', 90, 11.00, 'kg'),
(55, 6, 'Organic Malabar Black Pepper', 650.00, '2026-07-14', '2027-07-14', 70, 10.00, 'kg'),
(56, 6, 'Organic Green Cardamom (Elaichi)', 2200.00, '2026-07-15', '2027-07-15', 40, 12.00, 'kg'),
(57, 6, 'Organic Ceylon Cinnamon Sticks', 950.00, '2026-07-16', '2027-07-16', 60, 9.00, 'kg'),
(58, 6, 'Organic Malnad Whole Cloves (Laung)', 1100.00, '2026-07-17', '2027-07-17', 50, 12.00, 'kg'),
(59, 6, 'Organic Sweet Fennel Seeds (Saunf)', 190.00, '2026-07-18', '2027-07-18', 110, 9.00, 'kg'),
(60, 6, 'Organic Whole Fenugreek Seeds (Methi)', 140.00, '2026-07-19', '2027-07-19', 130, 10.00, 'kg'),
(61, 7, 'Organic Fresh Mixed Fruit Juice', 135.00, '2026-07-18', '2026-10-18', 60, 10.00, 'L'),
(62, 7, 'Organic Tender Coconut Water', 90.00, '2026-07-28', '2026-08-05', 120, 10.00, 'L'),
(63, 7, 'Organic Raw Sugarcane Juice', 80.00, '2026-07-28', '2026-08-02', 100, 11.00, 'L'),
(64, 7, 'Organic Cold-Pressed Wild Amla Juice', 160.00, '2026-07-20', '2026-11-20', 80, 11.00, 'L'),
(65, 7, 'Organic Konkan Kokum Sherbet Concentrate', 175.00, '2026-07-15', '2027-01-15', 70, 10.00, 'L'),
(66, 7, 'Organic Fresh Mint Lemonade', 85.00, '2026-07-27', '2026-08-05', 90, 10.00, 'L'),
(67, 7, 'Organic Traditional Nannari Roots Sherbet', 150.00, '2026-07-10', '2027-01-10', 75, 12.00, 'L'),
(68, 7, 'Organic Pure Aloe Vera Drink', 140.00, '2026-07-22', '2026-11-22', 85, 12.00, 'L'),
(69, 7, 'Organic Alphonso Mango Nectar Juice', 190.00, '2026-07-25', '2026-10-25', 80, 11.00, 'L'),
(70, 7, 'Organic Fresh Red Pomegranate Juice', 210.00, '2026-07-26', '2026-08-10', 65, 12.00, 'L'),
(71, 8, 'Organic Premium Almonds', 450.00, '2026-07-08', '2027-07-08', 90, 10.00, 'g'),
(72, 9, 'Organic Ancient Foxtail Millet', 160.00, '2026-07-14', '2027-01-14', 120, 0.00, 'kg'),
(73, 10, 'Organic Cold Pressed Mustard Oil', 320.00, '2026-07-22', '2027-07-22', 75, 8.00, 'L');

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

-- Wishlist Table (Replica of Cart)
CREATE TABLE IF NOT EXISTS Wishlist (
    wishlist_id INT AUTO_INCREMENT PRIMARY KEY,
    customer_id INT NOT NULL,
    product_id INT NOT NULL,
    product_count INT NOT NULL,
    product_price DECIMAL(10,2) NOT NULL,
    product_discount DECIMAL(5,2) NOT NULL,
    price_after_discount DECIMAL(10,2) NOT NULL,

    CONSTRAINT fk_wishlist_customer
        FOREIGN KEY (customer_id)
        REFERENCES Customer_Details(customer_id),

    CONSTRAINT fk_wishlist_product
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

