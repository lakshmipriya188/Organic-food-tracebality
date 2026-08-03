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
MYSQL_DATABASE = os.environ.get("MYSQL_DATABASE", "organic_food_traceability")

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
                unit VARCHAR(50) DEFAULT 'kg',
                manufacture_date DATE,
                expiry_date DATE,
                quantity INT,
                discount DECIMAL(5,2),
                onboarding_date DATE,
                manufacturer_name VARCHAR(100),
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
                order_time TIME NOT NULL,
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
                (1, 1, "Organic Fresh Fruits", 120.00, "kg", "2026-07-20", "2026-08-05", 50, 14.00, "2026-07-01", "Mandya Organic Fruit Orchards"),
                (2, 2, "Organic Farm Vegetables", 85.00, "kg", "2026-07-25", "2026-08-02", 100, 10.00, "2026-07-01", "Maddur Riverbank Farms"),
                (3, 3, "Organic Whole Grains", 150.00, "kg", "2026-07-10", "2027-07-10", 200, 0.00, "2026-07-01", "Mysuru Heritage Paddy Farms"),
                (4, 4, "Organic Native Pulses", 180.00, "kg", "2026-07-12", "2027-01-12", 150, 10.00, "2026-07-01", "Kalaburagi Pulse Collective"),
                (5, 5, "Organic Pure A2 Milk", 95.00, "L", "2026-07-28", "2026-07-31", 40, 0.00, "2026-07-01", "Pandavapura Bilona Dairy"),
                (6, 6, "Organic Aromatic Spices", 210.00, "250g", "2026-07-05", "2027-07-05", 80, 8.00, "2026-07-01", "Sirsi Spice Hills Garden"),
                (7, 7, "Organic Herbal Beverage", 135.00, "1L bottle", "2026-07-18", "2026-10-18", 60, 0.00, "2026-07-01", "Chikmagalur Herbal Valley"),
                (8, 8, "Organic Premium Almonds", 450.00, "500g", "2026-07-08", "2027-07-08", 90, 10.00, "2026-07-01", "Kolar Organic Nut Growers"),
                (9, 9, "Organic Ancient Foxtail Millet", 160.00, "kg", "2026-07-14", "2027-01-14", 120, 0.00, "2026-07-01", "Nagamangala Rainfed Farms"),
                (10, 10, "Organic Cold Pressed Mustard Oil", 320.00, "1L", "2026-07-22", "2027-07-22", 75, 8.00, "2026-07-01", "Challakere Wooden Ghani Mill"),
            ]
            cursor.executemany(
                """INSERT INTO Product 
                (product_id, category_id, product_name, price, unit, manufacture_date, expiry_date, quantity, discount, onboarding_date, manufacturer_name)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);""",
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
                      quantity, discount, onboarding_date, manufacturer_name
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
                      p.expiry_date, p.quantity, p.discount, p.onboarding_date, p.manufacturer_name,
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

    # Fallback in-memory check
    for fc in FALLBACK_CUSTOMERS:
        if fc["email_id"].lower() == clean_email and fc["password"] == password:
            return {"customer_id": fc["customer_id"], "customer_name": fc["customer_name"], "email_id": fc["email_id"]}
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
    """Fetch newest onboarding products using SQL:
    SELECT a.product_name, a.price, a.discount, a.price - a.discount FROM Product a ORDER BY onboarding_date desc LIMIT 10
    """
    try:
        conn = get_connection(include_db=True)
        cursor = conn.cursor(dictionary=True)
        query = """
            SELECT a.product_id, a.category_id, a.product_name, a.price, a.discount, (a.price - COALESCE(a.discount, 0)) AS price_after_discount, a.onboarding_date
            FROM Product a
            ORDER BY a.onboarding_date DESC, a.product_id DESC
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
                o.order_time,
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



