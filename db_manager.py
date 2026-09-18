"""MySQL Database Manager for Organic Food Traceability.

Handles connection to MySQL database (user: root, password: root123, port: 3306, db: organic_food_traceability)
and manages Category and Product tables.
"""

import os
from typing import List, Dict, Any, Optional
import mysql.connector
from mysql.connector import Error

# MySQL Connection Configurations
MYSQL_HOST = os.environ.get("MYSQL_HOST", "localhost")
MYSQL_PORT = int(os.environ.get("MYSQL_PORT", 3306))
MYSQL_USER = os.environ.get("MYSQL_USER", "root")
MYSQL_PASSWORD = os.environ.get("MYSQL_PASSWORD", "root123")
MYSQL_DATABASE = os.environ.get("MYSQL_DATABASE", "farmora")

# Default image mapping for category images
CATEGORY_IMAGES = {
    1: "assets/images/fruits.jpg",
    2: "assets/images/vegetables.jpg",
    3: "assets/images/grains.jpg",
    4: "assets/images/pulses.jpg",
    5: "assets/images/dairy.jpg",
    6: "assets/images/spices.jpg",
    7: "assets/images/beverages.jpg",
    8: "assets/images/dryfruit.jpg",
    9: "assets/images/millets.jpg",
    10: "assets/images/oils.jpg",
}

# Default slug mapping for category slugs
CATEGORY_SLUGS = {
    1: "fruits",
    2: "vegetables",
    3: "grains",
    4: "pulses",
    5: "dairy",
    6: "spices",
    7: "beverages",
    8: "dry-fruits",
    9: "millets",
    10: "oils",
}


def get_connection(include_db: bool = True):
    """Establish and return MySQL connection."""
    config = {
        "host": MYSQL_HOST,
        "port": MYSQL_PORT,
        "user": MYSQL_USER,
        "password": MYSQL_PASSWORD,
        "autocommit": True
    }
    if include_db:
        config["database"] = MYSQL_DATABASE
    return mysql.connector.connect(**config)


def init_mysql_db():
    """Ensure database, Category and Product tables exist and seed initial data if empty."""
    try:
        # Step 1: Connect without DB to ensure database exists
        conn = get_connection(include_db=False)
        cursor = conn.cursor()
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS `{MYSQL_DATABASE}`;")
        cursor.close()
        conn.close()

        # Step 2: Connect to organic_food_traceability DB and create tables
        conn = get_connection(include_db=True)
        cursor = conn.cursor()

        # Create Category Table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Category(
                category_id INT PRIMARY KEY AUTO_INCREMENT,
                category_name VARCHAR(100) NOT NULL,
                description TEXT
            );
        """)

        # Create Product Table
        cursor.execute("""
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
                FOREIGN KEY(category_id) REFERENCES Category(category_id) ON DELETE SET NULL
            );
        """)

        # Migration check for unit column in Product table
        cursor.execute("SHOW COLUMNS FROM Product LIKE 'unit';")
        if not cursor.fetchone():
            cursor.execute("ALTER TABLE Product ADD COLUMN unit VARCHAR(50) DEFAULT 'kg';")
            print("Added missing 'unit' column to Product table.")

        # Create Customer_Details Table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Customer_Details (
                customer_id INT AUTO_INCREMENT PRIMARY KEY,
                customer_name VARCHAR(100) NOT NULL,
                email_id VARCHAR(100) NOT NULL UNIQUE,
                password VARCHAR(255) NOT NULL
            );
        """)

        # Create Cart Table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Cart (
                cart_id INT AUTO_INCREMENT PRIMARY KEY,
                customer_id INT NOT NULL,
                product_id INT NOT NULL,
                product_count INT NOT NULL,
                product_price DECIMAL(10,2) NOT NULL,
                product_discount DECIMAL(5,2) NOT NULL,
                price_after_discount DECIMAL(10,2) NOT NULL,
                CONSTRAINT fk_cart_customer FOREIGN KEY (customer_id) REFERENCES Customer_Details(customer_id) ON DELETE CASCADE,
                CONSTRAINT fk_cart_product FOREIGN KEY (product_id) REFERENCES Product(product_id) ON DELETE CASCADE
            );
        """)

        # Create Wishlist Table (Replica of Cart)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Wishlist (
                wishlist_id INT AUTO_INCREMENT PRIMARY KEY,
                customer_id INT NOT NULL,
                product_id INT NOT NULL,
                product_count INT NOT NULL,
                product_price DECIMAL(10,2) NOT NULL,
                product_discount DECIMAL(5,2) NOT NULL,
                price_after_discount DECIMAL(10,2) NOT NULL,
                CONSTRAINT fk_wishlist_customer FOREIGN KEY (customer_id) REFERENCES Customer_Details(customer_id) ON DELETE CASCADE,
                CONSTRAINT fk_wishlist_product FOREIGN KEY (product_id) REFERENCES Product(product_id) ON DELETE CASCADE
            );
        """)

        # Create Order_Details Table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Order_Details (
                order_id INT AUTO_INCREMENT PRIMARY KEY,
                customer_id INT NOT NULL,
                product_id INT NOT NULL,
                product_count INT NOT NULL,
                product_price DECIMAL(10,2) NOT NULL,
                product_discount DECIMAL(5,2) NOT NULL,
                price_after_discount DECIMAL(10,2) NOT NULL,
                order_date DATE NOT NULL,
                CONSTRAINT fk_order_customer FOREIGN KEY (customer_id) REFERENCES Customer_Details(customer_id) ON DELETE CASCADE,
                CONSTRAINT fk_order_product FOREIGN KEY (product_id) REFERENCES Product(product_id) ON DELETE CASCADE
            );
        """)

        # Seed categories if empty
        cursor.execute("SELECT COUNT(*) FROM Category;")
        cat_count = cursor.fetchone()[0]
        if cat_count == 0:
            categories_data = [
                (1, "Fruits", "100% Organic Farm-Fresh Fruits"),
                (2, "Vegetables", "Fresh Organic Farm Vegetables"),
                (3, "Grains", "Unpolished Traditional Whole Grains"),
                (4, "Pulses", "Sun-dried Native Organic Pulses"),
                (5, "Dairy", "Pure A2 Desi Cow Dairy Products"),
                (6, "Spices", "Organic Aromatic Whole Spices"),
                (7, "Beverages", "Natural Organic Drinks & Juices"),
                (8, "Dry Fruits", "Premium Raw Organic Dry Fruits"),
                (9, "Millets", "Nutrient-rich Ancient Organic Millets"),
                (10, "Oils", "Traditional Wooden Cold-Pressed Oils"),
            ]
            cursor.executemany(
                "INSERT INTO Category (category_id, category_name, description) VALUES (%s, %s, %s);",
                categories_data
            )
            print(f"Seeded {len(categories_data)} categories into MySQL Category table.")

        # Seed products if empty
        cursor.execute("SELECT COUNT(*) FROM Product;")
        prod_count = cursor.fetchone()[0]
        if prod_count == 0:
            products_data = [
                # Category 1: 10 Fruits (all unit = kg)
                (1, 1, "Organic Royal Gala Apple", 180.00, "2026-07-20", "2026-08-05", 50, 10.00, "kg"),
                (2, 1, "Organic Robusta Banana", 60.00, "2026-07-22", "2026-07-30", 80, 8.00, "kg"),
                (3, 1, "Organic Alphonso Mango", 350.00, "2026-07-15", "2026-07-28", 40, 12.00, "kg"),
                (4, 1, "Organic Nagpur Orange", 90.00, "2026-07-18", "2026-08-08", 60, 10.00, "kg"),
                (5, 1, "Organic Red Pomegranate", 220.00, "2026-07-19", "2026-08-15", 45, 12.00, "kg"),
                (6, 1, "Organic Pink Guava", 80.00, "2026-07-21", "2026-08-01", 55, 6.00, "kg"),
                (7, 1, "Organic Hybrid Watermelon", 40.00, "2026-07-24", "2026-08-10", 70, 10.00, "kg"),
                (8, 1, "Organic Pink Dragon Fruit", 250.00, "2026-07-23", "2026-08-07", 30, 14.00, "kg"),
                (9, 1, "Organic Queen Pineapple", 110.00, "2026-07-17", "2026-08-07", 40, 8.00, "kg"),
                (10, 1, "Organic Sweet Lime (Mosambi)", 95.00, "2026-07-20", "2026-08-10", 50, 9.00, "kg"),
                # Category 2: 10 Vegetables (all unit = kg)
                (11, 2, "Organic Country Tomato", 45.00, "2026-07-25", "2026-08-05", 100, 10.00, "kg"),
                (12, 2, "Organic Fresh Potato", 35.00, "2026-07-20", "2026-08-20", 120, 12.00, "kg"),
                (13, 2, "Organic Red Onion", 40.00, "2026-07-18", "2026-08-30", 150, 11.00, "kg"),
                (14, 2, "Organic Farm Carrot", 60.00, "2026-07-24", "2026-08-10", 90, 14.00, "kg"),
                (15, 2, "Organic Green Cabbage", 30.00, "2026-07-26", "2026-08-08", 80, 14.00, "kg"),
                (16, 2, "Organic Fresh Cauliflower", 50.00, "2026-07-25", "2026-08-03", 70, 9.00, "kg"),
                (17, 2, "Organic Green Capsicum", 80.00, "2026-07-23", "2026-08-04", 65, 11.00, "kg"),
                (18, 2, "Organic Purple Brinjal", 40.00, "2026-07-22", "2026-08-02", 75, 11.00, "kg"),
                (19, 2, "Organic Ruby Beetroot", 50.00, "2026-07-21", "2026-08-15", 85, 9.00, "kg"),
                (20, 2, "Organic Sweet Corn", 45.00, "2026-07-24", "2026-08-06", 110, 10.00, "kg"),
                # Category 3: 10 Grains (all unit = kg)
                (21, 3, "Organic Unpolished Brown Rice", 150.00, "2026-07-10", "2027-07-10", 200, 14.00, "kg"),
                (22, 3, "Organic Khapli Whole Wheat", 85.00, "2026-07-12", "2027-07-12", 250, 10.00, "kg"),
                (23, 3, "Organic Pearl Barley Grain", 110.00, "2026-07-14", "2027-07-14", 140, 12.00, "kg"),
                (24, 3, "Organic Raw Buckwheat (Kuttu)", 160.00, "2026-07-16", "2027-07-16", 110, 11.00, "kg"),
                (25, 3, "Organic White Quinoa Grain", 280.00, "2026-07-18", "2027-07-18", 90, 12.00, "kg"),
                (26, 3, "Organic Whole Rolled Oats", 190.00, "2026-07-20", "2027-07-20", 130, 9.00, "kg"),
                (27, 3, "Organic Whole Rye Grain", 140.00, "2026-07-22", "2027-07-22", 100, 10.00, "kg"),
                (28, 3, "Organic Jowar Whole Grain", 95.00, "2026-07-15", "2027-07-15", 180, 9.00, "kg"),
                (29, 3, "Organic Traditional Basmati Rice", 220.00, "2026-07-11", "2027-07-11", 160, 12.00, "kg"),
                (30, 3, "Organic Kerala Red Matta Rice", 130.00, "2026-07-13", "2027-07-13", 150, 10.00, "kg"),
                # Category 4: 10 Pulses (all unit = kg)
                (31, 4, "Organic Unpolished Toor Dal (Arhar)", 180.00, "2026-07-12", "2027-01-12", 150, 10.00, "kg"),
                (32, 4, "Organic Split Red Lentil (Masoor Dal)", 140.00, "2026-07-14", "2027-01-14", 160, 10.00, "kg"),
                (33, 4, "Organic Kabuli Chickpeas (Chana)", 160.00, "2026-07-15", "2027-01-15", 140, 11.00, "kg"),
                (34, 4, "Organic Whole Black Gram (Urad Whole)", 175.00, "2026-07-18", "2027-01-18", 130, 10.00, "kg"),
                (35, 4, "Organic Whole Green Moong Dal", 155.00, "2026-07-16", "2027-01-16", 170, 9.00, "kg"),
                (36, 4, "Organic Native Horse Gram (Kollu)", 120.00, "2026-07-13", "2027-01-13", 120, 11.00, "kg"),
                (37, 4, "Organic Brown Cowpeas (Lobia)", 130.00, "2026-07-17", "2027-01-17", 110, 10.00, "kg"),
                (38, 4, "Organic Kashmiri Rajma (Kidney Beans)", 195.00, "2026-07-19", "2027-01-19", 100, 11.00, "kg"),
                (39, 4, "Organic Dried White Peas (Safed Matar)", 110.00, "2026-07-21", "2027-01-21", 125, 12.00, "kg"),
                (40, 4, "Organic Native Yellow Soybeans", 135.00, "2026-07-20", "2027-01-20", 135, 10.00, "kg"),
                # Category 5: 10 Dairy Products (all unit = L)
                (41, 5, "Organic Pure A2 Desi Cow Milk", 95.00, "2026-07-28", "2026-07-31", 100, 14.00, "L"),
                (42, 5, "Organic Farm Fresh Buffalo Milk", 85.00, "2026-07-28", "2026-07-31", 120, 10.00, "L"),
                (43, 5, "Organic Badam Flavoured Milk", 140.00, "2026-07-26", "2026-08-05", 80, 12.00, "L"),
                (44, 5, "Organic Traditional Spiced Buttermilk (Chaas)", 60.00, "2026-07-27", "2026-08-02", 150, 14.00, "L"),
                (45, 5, "Organic A2 Desi Cow Bilona Ghee", 1450.00, "2026-07-15", "2027-07-15", 60, 9.00, "L"),
                (46, 5, "Organic Fresh Creamy Set Curd (Dahi)", 110.00, "2026-07-27", "2026-08-03", 90, 12.00, "L"),
                (47, 5, "Organic Raw Almond Milk", 220.00, "2026-07-26", "2026-08-04", 70, 12.00, "L"),
                (48, 5, "Organic Fresh Farm Malai Cream", 350.00, "2026-07-27", "2026-08-02", 50, 10.00, "L"),
                (49, 5, "Organic Kesar Pista Flavoured Milk", 160.00, "2026-07-26", "2026-08-05", 75, 11.00, "L"),
                (50, 5, "Organic Sweet Mango Lassi", 120.00, "2026-07-27", "2026-08-03", 85, 11.00, "L"),
                # Category 6: 10 Spices (all unit = kg)
                (51, 6, "Organic Salem Whole Turmeric & Powder", 210.00, "2026-07-05", "2027-07-05", 80, 8.00, "kg"),
                (52, 6, "Organic Guntur Red Chilli Powder", 280.00, "2026-07-08", "2027-07-08", 100, 10.00, "kg"),
                (53, 6, "Organic Native Coriander Seeds (Dhania)", 160.00, "2026-07-10", "2027-07-10", 120, 11.00, "kg"),
                (54, 6, "Organic Whole Cumin Seeds (Jeera)", 320.00, "2026-07-12", "2027-07-12", 90, 11.00, "kg"),
                (55, 6, "Organic Malabar Black Pepper", 650.00, "2026-07-14", "2027-07-14", 70, 10.00, "kg"),
                (56, 6, "Organic Green Cardamom (Elaichi)", 2200.00, "2026-07-15", "2027-07-15", 40, 12.00, "kg"),
                (57, 6, "Organic Ceylon Cinnamon Sticks", 950.00, "2026-07-16", "2027-07-16", 60, 9.00, "kg"),
                (58, 6, "Organic Malnad Whole Cloves (Laung)", 1100.00, "2026-07-17", "2027-07-17", 50, 12.00, "kg"),
                (59, 6, "Organic Sweet Fennel Seeds (Saunf)", 190.00, "2026-07-18", "2027-07-18", 110, 9.00, "kg"),
                (60, 6, "Organic Whole Fenugreek Seeds (Methi)", 140.00, "2026-07-19", "2027-07-19", 130, 10.00, "kg"),
                # Category 7: 10 Beverages (all unit = L)
                (61, 7, "Organic Fresh Mixed Fruit Juice", 135.00, "2026-07-18", "2026-10-18", 60, 10.00, "L"),
                (62, 7, "Organic Tender Coconut Water", 90.00, "2026-07-28", "2026-08-05", 120, 10.00, "L"),
                (63, 7, "Organic Raw Sugarcane Juice", 80.00, "2026-07-28", "2026-08-02", 100, 11.00, "L"),
                (64, 7, "Organic Cold-Pressed Wild Amla Juice", 160.00, "2026-07-20", "2026-11-20", 80, 11.00, "L"),
                (65, 7, "Organic Konkan Kokum Sherbet Concentrate", 175.00, "2026-07-15", "2027-01-15", 70, 10.00, "L"),
                (66, 7, "Organic Fresh Mint Lemonade", 85.00, "2026-07-27", "2026-08-05", 90, 10.00, "L"),
                (67, 7, "Organic Traditional Nannari Roots Sherbet", 150.00, "2026-07-10", "2027-01-10", 75, 12.00, "L"),
                (68, 7, "Organic Pure Aloe Vera Drink", 140.00, "2026-07-22", "2026-11-22", 85, 12.00, "L"),
                (69, 7, "Organic Alphonso Mango Nectar Juice", 190.00, "2026-07-25", "2026-10-25", 80, 11.00, "L"),
                (70, 7, "Organic Fresh Red Pomegranate Juice", 210.00, "2026-07-26", "2026-08-10", 65, 12.00, "L"),
                # Other Categories
                (71, 8, "Organic Premium Almonds", 450.00, "2026-07-08", "2027-07-08", 90, 10.00, "g"),
                (72, 9, "Organic Ancient Foxtail Millet", 160.00, "2026-07-14", "2027-01-14", 120, 0.00, "kg"),
                (73, 10, "Organic Cold Pressed Mustard Oil", 320.00, "2026-07-22", "2027-07-22", 75, 8.00, "L"),
            ]
            cursor.executemany(
                """INSERT INTO Product 
                (product_id, category_id, product_name, price, manufacture_date, expiry_date, quantity, discount, unit)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s);""",
                products_data
            )
            print(f"Seeded {len(products_data)} products into MySQL Product table.")

        # Seed Customer_Details if empty
        cursor.execute("SELECT COUNT(*) FROM Customer_Details;")
        cust_count = cursor.fetchone()[0]
        if cust_count == 0:
            customers_data = [
                ("Rahul Sharma", "rahul@gmail.com", "Rahul@123"),
                ("Priya Singh", "priya@gmail.com", "Priya@123"),
                ("Amit Kumar", "amit@gmail.com", "Amit@123"),
                ("Sneha Reddy", "sneha@gmail.com", "Sneha@123"),
                ("Arjun Patel", "arjun@gmail.com", "Arjun@123"),
            ]
            cursor.executemany(
                "INSERT INTO Customer_Details (customer_name, email_id, password) VALUES (%s, %s, %s);",
                customers_data
            )
            print(f"Seeded {len(customers_data)} customers into MySQL Customer_Details table.")

        cursor.close()
        conn.close()
        return True
    except Error as e:
        print(f"MySQL DB Error: {e}")
        return False


def fetch_all_categories_db() -> List[Dict[str, Any]]:
    """Fetch all rows from MySQL Category table."""
    try:
        conn = get_connection(include_db=True)
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT category_id, category_name, description FROM Category ORDER BY category_id ASC;")
        rows = cursor.fetchall()
        cursor.close()
        conn.close()
        return rows
    except Error as e:
        print(f"Error fetching categories: {e}")
        return []


def fetch_products_by_category_db(category_id: int) -> List[Dict[str, Any]]:
    """Fetch products matching category_id from MySQL Product table."""
    try:
        conn = get_connection(include_db=True)
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            """SELECT product_id, category_id, product_name, price, unit, manufacture_date, expiry_date,
                      quantity, discount
               FROM Product
               WHERE category_id = %s
               ORDER BY product_id ASC;""",
            (category_id,)
        )
        rows = cursor.fetchall()
        cursor.close()
        conn.close()
        return rows
    except Error as e:
        print(f"Error fetching products for category_id {category_id}: {e}")
        return []


def fetch_all_products_db() -> List[Dict[str, Any]]:
    """Fetch all rows from MySQL Product table."""
    try:
        conn = get_connection(include_db=True)
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            """SELECT p.product_id, p.category_id, p.product_name, p.price, p.unit, p.manufacture_date,
                      p.expiry_date, p.quantity, p.discount,
                      c.category_name
               FROM Product p
               LEFT JOIN Category c ON p.category_id = c.category_id
               ORDER BY p.product_id ASC;"""
        )
        rows = cursor.fetchall()
        cursor.close()
        conn.close()
        return rows
    except Error as e:
        print(f"Error fetching all products: {e}")
        return []


def update_product_db(
    product_id: int,
    product_name: str,
    price: float,
    discount: float,
    quantity: Optional[int] = None,
    unit: Optional[str] = None,
    manufacture_date: Optional[str] = None,
    expiry_date: Optional[str] = None
) -> tuple[bool, str]:
    """Update an existing product record in the MySQL Product table."""
    try:
        conn = get_connection(include_db=True)
        cursor = conn.cursor(dictionary=True)

        cursor.execute("SELECT product_id FROM Product WHERE product_id = %s;", (int(product_id),))
        row = cursor.fetchone()
        if not row:
            cursor.close()
            conn.close()
            return False, f"Product ID #{product_id} not found in database."

        update_fields = ["product_name = %s", "price = %s", "discount = %s"]
        params = [product_name.strip(), float(price), float(discount)]

        if quantity is not None:
            update_fields.append("quantity = %s")
            params.append(int(quantity))
        if unit:
            update_fields.append("unit = %s")
            params.append(unit.strip())
        if manufacture_date:
            update_fields.append("manufacture_date = %s")
            params.append(str(manufacture_date).strip())
        if expiry_date:
            update_fields.append("expiry_date = %s")
            params.append(str(expiry_date).strip())

        params.append(int(product_id))
        query = f"UPDATE Product SET {', '.join(update_fields)} WHERE product_id = %s;"

        cursor.execute(query, params)
        conn.commit()
        cursor.close()
        conn.close()
        return True, "Product updated successfully!"
    except Error as e:
        print(f"MySQL error during update_product_db: {e}")
        return False, f"Database update error: {e}"


# Default fallback customers matching Customer_Details table
FALLBACK_CUSTOMERS = [
    {"customer_id": 1, "customer_name": "Rahul Sharma", "email_id": "rahul@gmail.com", "password": "Rahul@123"},
    {"customer_id": 2, "customer_name": "Priya Singh", "email_id": "priya@gmail.com", "password": "Priya@123"},
    {"customer_id": 3, "customer_name": "Amit Kumar", "email_id": "amit@gmail.com", "password": "Amit@123"},
    {"customer_id": 4, "customer_name": "Sneha Reddy", "email_id": "sneha@gmail.com", "password": "Sneha@123"},
    {"customer_id": 5, "customer_name": "Arjun Patel", "email_id": "arjun@gmail.com", "password": "Arjun@123"},
]


def fetch_all_customers_db() -> List[Dict[str, Any]]:
    """Fetch all rows from Customer_Details table, or fallback list if DB unavailable."""
    try:
        conn = get_connection(include_db=True)
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT customer_id, customer_name, email_id, password FROM Customer_Details ORDER BY customer_id ASC;")
        rows = cursor.fetchall()
        cursor.close()
        conn.close()
        return rows if rows else FALLBACK_CUSTOMERS
    except Error as e:
        print(f"Error fetching customers from MySQL DB: {e}")
        return FALLBACK_CUSTOMERS


def verify_customer_login(email_id: str, password: str) -> Optional[Dict[str, Any]]:
    """Verify email and password against Customer_Details database table (or fallback list)."""
    clean_email = email_id.strip().lower()
    try:
        conn = get_connection(include_db=True)
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            "SELECT customer_id, customer_name, email_id FROM Customer_Details WHERE LOWER(email_id) = %s AND password = %s;",
            (clean_email, password)
        )
        user = cursor.fetchone()
        cursor.close()
        conn.close()
        if user:
            return user
    except Error as e:
        print(f"MySQL error during verify_customer_login: {e}")

    for fc in FALLBACK_CUSTOMERS:
        if fc["email_id"].lower() == clean_email and fc["password"] == password:
            return {"customer_id": fc["customer_id"], "customer_name": fc["customer_name"], "email_id": fc["email_id"]}
    return None


def get_customer_by_email(email_id: str) -> Optional[Dict[str, Any]]:
    """Fetch customer record from Customer_Details by email ID (without password check)."""
    clean_email = email_id.strip().lower()
    try:
        conn = get_connection(include_db=True)
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            "SELECT customer_id, customer_name, email_id, password FROM Customer_Details WHERE LOWER(email_id) = %s;",
            (clean_email,)
        )
        user = cursor.fetchone()
        cursor.close()
        conn.close()
        if user:
            return user
    except Error as e:
        print(f"MySQL error during get_customer_by_email: {e}")

    for fc in FALLBACK_CUSTOMERS:
        if fc["email_id"].lower() == clean_email:
            return fc
    return None


def register_customer(customer_name: str, email_id: str, password: str) -> tuple[bool, str, Optional[Dict[str, Any]]]:
    """Insert a new customer into Customer_Details table (and fallback list)."""
    clean_email = email_id.strip().lower()
    clean_name = customer_name.strip()

    # Try MySQL DB insertion
    try:
        conn = get_connection(include_db=True)
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT customer_id FROM Customer_Details WHERE LOWER(email_id) = %s;", (clean_email,))
        existing = cursor.fetchone()
        if existing:
            cursor.close()
            conn.close()
            return False, "An account with this email address already exists.", None

        cursor.execute(
            "INSERT INTO Customer_Details (customer_name, email_id, password) VALUES (%s, %s, %s);",
            (clean_name, clean_email, password)
        )
        new_id = cursor.lastrowid
        cursor.close()
        conn.close()

        new_cust = {"customer_id": new_id, "customer_name": clean_name, "email_id": clean_email}
        # Also add to fallback
        FALLBACK_CUSTOMERS.append({"customer_id": new_id, "customer_name": clean_name, "email_id": clean_email, "password": password})
        return True, "Account created successfully!", new_cust
    except Error as e:
        print(f"MySQL error during register_customer: {e}")
        # Fallback registration
        for fc in FALLBACK_CUSTOMERS:
            if fc["email_id"].lower() == clean_email:
                return False, "An account with this email address already exists.", None
        new_id = len(FALLBACK_CUSTOMERS) + 1
        new_cust = {"customer_id": new_id, "customer_name": clean_name, "email_id": clean_email}
        FALLBACK_CUSTOMERS.append({"customer_id": new_id, "customer_name": clean_name, "email_id": clean_email, "password": password})
        return True, "Account created successfully!", new_cust


def fetch_cart_items_db(customer_id: int) -> List[Dict[str, Any]]:
    """Fetch cart items for a specific customer from MySQL Cart table joined with Product & Category."""
    try:
        conn = get_connection(include_db=True)
        cursor = conn.cursor(dictionary=True)
        query = """
            SELECT 
                c.cart_id,
                c.customer_id,
                c.product_id,
                c.product_count,
                c.product_price,
                c.product_discount,
                c.price_after_discount,
                p.product_name,
                cat.category_name,
                cat.category_id
            FROM Cart c
            JOIN Product p ON c.product_id = p.product_id
            LEFT JOIN Category cat ON p.category_id = cat.category_id
            WHERE c.customer_id = %s
            ORDER BY c.cart_id ASC;
        """
        cursor.execute(query, (customer_id,))
        items = cursor.fetchall()
        cursor.close()
        conn.close()
        return items
    except Error as e:
        print(f"MySQL error fetching cart items: {e}")
        return []


def add_or_update_cart_db(customer_id: int, product_id: int, count: int, price: float, discount: float) -> bool:
    """Add product to customer's cart or increment product_count if already exists."""
    price_after_disc = round(price * (1 - (discount / 100.0)), 2)
    try:
        conn = get_connection(include_db=True)
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            "SELECT cart_id, product_count FROM Cart WHERE customer_id = %s AND product_id = %s;",
            (customer_id, product_id)
        )
        existing = cursor.fetchone()
        if existing:
            new_count = existing["product_count"] + count
            cursor.execute(
                "UPDATE Cart SET product_count = %s, product_price = %s, product_discount = %s, price_after_discount = %s WHERE cart_id = %s;",
                (new_count, price, discount, price_after_disc, existing["cart_id"])
            )
        else:
            cursor.execute(
                """INSERT INTO Cart 
                (customer_id, product_id, product_count, product_price, product_discount, price_after_discount)
                VALUES (%s, %s, %s, %s, %s, %s);""",
                (customer_id, product_id, count, price, discount, price_after_disc)
            )
        cursor.close()
        conn.close()
        return True
    except Error as e:
        print(f"MySQL error adding/updating cart: {e}")
        return False


def update_cart_count_db(customer_id: int, product_id: int, new_count: int) -> bool:
    """Update product_count or delete if count <= 0."""
    try:
        conn = get_connection(include_db=True)
        cursor = conn.cursor()
        if new_count <= 0:
            cursor.execute("DELETE FROM Cart WHERE customer_id = %s AND product_id = %s;", (customer_id, product_id))
        else:
            cursor.execute("UPDATE Cart SET product_count = %s WHERE customer_id = %s AND product_id = %s;", (new_count, customer_id, product_id))
        cursor.close()
        conn.close()
        return True
    except Error as e:
        print(f"MySQL error updating cart count: {e}")
        return False


def remove_from_cart_db(customer_id: int, product_id: int) -> bool:
    """Remove product from customer's cart."""
    try:
        conn = get_connection(include_db=True)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM Cart WHERE customer_id = %s AND product_id = %s;", (customer_id, product_id))
        cursor.close()
        conn.close()
        return True
    except Error as e:
        print(f"MySQL error removing from cart: {e}")
        return False


def clear_cart_db(customer_id: int) -> bool:
    """Clear all items from customer's cart."""
    try:
        conn = get_connection(include_db=True)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM Cart WHERE customer_id = %s;", (customer_id,))
        cursor.close()
        conn.close()
        return True
    except Error as e:
        print(f"MySQL error clearing cart: {e}")
        return False


def fetch_wishlist_items_db(customer_id: int) -> List[Dict[str, Any]]:
    """Fetch wishlist items for a specific customer from MySQL Wishlist table joined with Product & Category."""
    try:
        conn = get_connection(include_db=True)
        cursor = conn.cursor(dictionary=True)
        query = """
            SELECT 
                w.wishlist_id,
                w.customer_id,
                w.product_id,
                w.product_count,
                w.product_price,
                w.product_discount,
                w.price_after_discount,
                p.product_name,
                cat.category_name,
                cat.category_id
            FROM Wishlist w
            JOIN Product p ON w.product_id = p.product_id
            LEFT JOIN Category cat ON p.category_id = cat.category_id
            WHERE w.customer_id = %s
            ORDER BY w.wishlist_id ASC;
        """
        cursor.execute(query, (customer_id,))
        items = cursor.fetchall()
        cursor.close()
        conn.close()
        return items
    except Error as e:
        print(f"MySQL error fetching wishlist items: {e}")
        return []


def add_or_update_wishlist_db(customer_id: int, product_id: int, count: int, price: float, discount: float) -> bool:
    """Add product to customer's wishlist or increment product_count if already exists."""
    price_after_disc = round(price * (1 - (discount / 100.0)), 2)
    try:
        conn = get_connection(include_db=True)
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            "SELECT wishlist_id, product_count FROM Wishlist WHERE customer_id = %s AND product_id = %s;",
            (customer_id, product_id)
        )
        existing = cursor.fetchone()
        if existing:
            new_count = existing["product_count"] + count
            cursor.execute(
                "UPDATE Wishlist SET product_count = %s, product_price = %s, product_discount = %s, price_after_discount = %s WHERE wishlist_id = %s;",
                (new_count, price, discount, price_after_disc, existing["wishlist_id"])
            )
        else:
            cursor.execute(
                """INSERT INTO Wishlist 
                (customer_id, product_id, product_count, product_price, product_discount, price_after_discount)
                VALUES (%s, %s, %s, %s, %s, %s);""",
                (customer_id, product_id, count, price, discount, price_after_disc)
            )
        cursor.close()
        conn.close()
        return True
    except Error as e:
        print(f"MySQL error adding/updating wishlist: {e}")
        return False


def update_wishlist_count_db(customer_id: int, product_id: int, new_count: int) -> bool:
    """Update product_count or delete if count <= 0."""
    try:
        conn = get_connection(include_db=True)
        cursor = conn.cursor()
        if new_count <= 0:
            cursor.execute("DELETE FROM Wishlist WHERE customer_id = %s AND product_id = %s;", (customer_id, product_id))
        else:
            cursor.execute("UPDATE Wishlist SET product_count = %s WHERE customer_id = %s AND product_id = %s;", (new_count, customer_id, product_id))
        cursor.close()
        conn.close()
        return True
    except Error as e:
        print(f"MySQL error updating wishlist count: {e}")
        return False


def remove_from_wishlist_db(customer_id: int, product_id: int) -> bool:
    """Remove product from customer's wishlist."""
    try:
        conn = get_connection(include_db=True)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM Wishlist WHERE customer_id = %s AND product_id = %s;", (customer_id, product_id))
        cursor.close()
        conn.close()
        return True
    except Error as e:
        print(f"MySQL error removing from wishlist: {e}")
        return False


def clear_wishlist_db(customer_id: int) -> bool:
    """Clear all items from customer's wishlist."""
    try:
        conn = get_connection(include_db=True)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM Wishlist WHERE customer_id = %s;", (customer_id,))
        cursor.close()
        conn.close()
        return True
    except Error as e:
        print(f"MySQL error clearing wishlist: {e}")
        return False


def checkout_order_db(customer_id: int) -> bool:
    """Copy all items from Cart table into Order_Details table with date/time, then clear Cart."""
    try:
        conn = get_connection(include_db=True)
        cursor = conn.cursor(dictionary=True)
        
        # 1. Fetch current cart items
        cursor.execute(
            "SELECT customer_id, product_id, product_count, product_price, product_discount, price_after_discount FROM Cart WHERE customer_id = %s;",
            (customer_id,)
        )
        cart_rows = cursor.fetchall()
        
        if not cart_rows:
            cursor.close()
            conn.close()
            return True

        # 2. Insert items into Order_Details with current date and time
        insert_query = """
            INSERT INTO Order_Details 
            (customer_id, product_id, product_count, product_price, product_discount, price_after_discount, order_date, order_time)
            VALUES (%s, %s, %s, %s, %s, %s, CURDATE(), CURTIME());
        """
        for r in cart_rows:
            cursor.execute(insert_query, (
                r["customer_id"],
                r["product_id"],
                r["product_count"],
                r["product_price"],
                r["product_discount"],
                r["price_after_discount"]
            ))

        # 3. Clear customer's Cart table
        cursor.execute("DELETE FROM Cart WHERE customer_id = %s;", (customer_id,))
        
        cursor.close()
        conn.close()
        return True
    except Error as e:
        print(f"MySQL error during checkout_order_db: {e}")
        return False


def fetch_bestsellers_db() -> List[Dict[str, Any]]:
    """Fetch top ordered bestsellers using user's exact SQL query joining Product and Order_Details."""
    try:
        conn = get_connection(include_db=True)
        cursor = conn.cursor(dictionary=True)
        query = """
            SELECT a.product_id, a.category_id, a.product_name, a.price, a.discount, (a.price - COALESCE(a.discount, 0)) AS price_after_discount
            FROM Product a
            JOIN (
                SELECT a.product_id, COUNT(*) AS order_cnt 
                FROM Order_Details a 
                JOIN Product b ON a.product_id = b.product_id
                GROUP BY 1 
                LIMIT 10
            ) b ON a.product_id = b.product_id;
        """
        cursor.execute(query)
        rows = cursor.fetchall()
        cursor.close()
        conn.close()
        return rows
    except Error as e:
        print(f"MySQL error fetching bestsellers: {e}")
        return []


def fetch_deals_db() -> List[Dict[str, Any]]:
    """Fetch top discounted products using SQL:
    SELECT a.product_name, a.price, a.discount, a.price - a.discount FROM Product a ORDER BY 3 desc LIMIT 10
    """
    try:
        conn = get_connection(include_db=True)
        cursor = conn.cursor(dictionary=True)
        query = """
            SELECT a.product_id, a.category_id, a.product_name, a.price, a.discount, (a.price - COALESCE(a.discount, 0)) AS price_after_discount
            FROM Product a
            ORDER BY 5 DESC
            LIMIT 10;
        """
        cursor.execute(query)
        rows = cursor.fetchall()
        cursor.close()
        conn.close()
        return rows
    except Error as e:
        print(f"MySQL error fetching deals: {e}")
        return []


def fetch_new_arrivals_db() -> List[Dict[str, Any]]:
    """Fetch newest products using SQL ordering by manufacture_date."""
    try:
        conn = get_connection(include_db=True)
        cursor = conn.cursor(dictionary=True)
        query = """
            SELECT a.product_id, a.category_id, a.product_name, a.price, a.discount, (a.price - COALESCE(a.discount, 0)) AS price_after_discount, a.manufacture_date
            FROM Product a
            ORDER BY a.manufacture_date DESC, a.product_id DESC
            LIMIT 10;
        """
        cursor.execute(query)
        rows = cursor.fetchall()
        cursor.close()
        conn.close()
        return rows
    except Error as e:
        print(f"MySQL error fetching new arrivals: {e}")
        return []


def fetch_order_history_db(customer_id: int) -> List[Dict[str, Any]]:
    """Fetch order history for a customer from Order_Details joined with Product & Category."""
    try:
        conn = get_connection(include_db=True)
        cursor = conn.cursor(dictionary=True)
        query = """
            SELECT 
                o.order_id,
                o.customer_id,
                o.product_id,
                o.product_count,
                o.product_price,
                o.product_discount,
                o.price_after_discount,
                o.order_date,
                p.product_name,
                p.unit,
                cat.category_name
            FROM Order_Details o
            JOIN Product p ON o.product_id = p.product_id
            LEFT JOIN Category cat ON p.category_id = cat.category_id
            WHERE o.customer_id = %s
            ORDER BY o.order_id DESC;
        """
        cursor.execute(query, (customer_id,))
        orders = cursor.fetchall()
        cursor.close()
        conn.close()
        return orders
    except Error as e:
        print(f"MySQL error fetching order history for customer_id {customer_id}: {e}")
        return []


def fetch_all_orders_db() -> List[Dict[str, Any]]:
    """Fetch all orders from Order_Details table joined with Product & Customer_Details."""
    try:
        conn = get_connection(include_db=True)
        cursor = conn.cursor(dictionary=True)
        query = """
            SELECT 
                o.order_id,
                o.customer_id,
                c.customer_name,
                c.email_id,
                o.product_id,
                p.product_name,
                p.unit,
                o.product_count,
                o.product_price,
                o.product_discount,
                o.price_after_discount,
                o.order_date,
                o.order_time
            FROM Order_Details o
            LEFT JOIN Product p ON o.product_id = p.product_id
            LEFT JOIN Customer_Details c ON o.customer_id = c.customer_id
            ORDER BY o.order_id DESC;
        """
        cursor.execute(query)
        orders = cursor.fetchall()
        cursor.close()
        conn.close()
        return orders
    except Error as e:
        print(f"MySQL error fetching all orders: {e}")
        return []



