"""Database initializer for Organic Food Traceability application (MySQL)."""

from db_manager import init_mysql_db, fetch_all_categories_db, fetch_all_products_db, fetch_all_customers_db

def init_db():
    print("Initializing MySQL Database (User: root, Port: 3306, DB: organic_food_traceability)...")
    success = init_mysql_db()
    if success:
        print("Successfully initialized MySQL database tables.")
        categories = fetch_all_categories_db()
        print(f"\nCategories in MySQL Category Table ({len(categories)} rows):")
        for cat in categories:
            print(f"  ID: {cat['category_id']} | Name: {cat['category_name']} | Description: {cat['description']}")

        products = fetch_all_products_db()
        print(f"\nProducts in MySQL Product Table ({len(products)} rows):")
        for prod in products:
            print(f"  ID: {prod['product_id']} | CatID: {prod['category_id']} | Name: {prod['product_name']} | Price: {prod['price']} | Mfr: {prod['manufacturer_name']}")

        customers = fetch_all_customers_db()
        print(f"\nCustomers in Customer_Details Table ({len(customers)} rows):")
        for cust in customers:
            print(f"  ID: {cust['customer_id']} | Name: {cust['customer_name']} | Email: {cust['email_id']}")
    else:
        print("Failed to connect to MySQL database. Please verify MySQL service is running on port 3306 with password root123.")

if __name__ == "__main__":
    init_db()

