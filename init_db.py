import os

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

from db_manager import init_mysql_db, fetch_all_categories_db, fetch_all_products_db, fetch_all_customers_db

def init_db():
    db_host = os.environ.get("MYSQL_HOST", "database-1.cl84msuko0wj.eu-north-1.rds.amazonaws.com")
    db_name = os.environ.get("MYSQL_DATABASE", "farmora")
    print(f"Initializing MySQL Database on {db_host} (DB: {db_name})...")
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
            print(f"  ID: {prod['product_id']} | CatID: {prod['category_id']} | Name: {prod['product_name']} | Price: {prod['price']} | Mfr: {prod.get('manufacturer_name', 'N/A')}")

        customers = fetch_all_customers_db()
        print(f"\nCustomers in Customer_Details Table ({len(customers)} rows):")
        for cust in customers:
            print(f"  ID: {cust['customer_id']} | Name: {cust['customer_name']} | Email: {cust['email_id']}")
    else:
        print(f"Failed to connect to MySQL database at {db_host}. Please verify database network accessibility and environment credentials.")

if __name__ == "__main__":
    init_db()

