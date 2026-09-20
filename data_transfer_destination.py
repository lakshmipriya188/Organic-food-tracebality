import os
import pymysql

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

# ============================================
# SOURCE DATABASE (Loaded from .env / env vars)
# ============================================

SOURCE_HOST = os.environ.get("SOURCE_MYSQL_HOST", os.environ.get("MYSQL_HOST", "localhost"))
SOURCE_PORT = int(os.environ.get("SOURCE_MYSQL_PORT", os.environ.get("MYSQL_PORT", 3306)))
SOURCE_USER = os.environ.get("SOURCE_MYSQL_USER", os.environ.get("MYSQL_USER", "root"))
SOURCE_PASSWORD = os.environ.get("SOURCE_MYSQL_PASSWORD", os.environ.get("MYSQL_PASSWORD", ""))
SOURCE_DATABASE = os.environ.get("SOURCE_MYSQL_DATABASE", os.environ.get("MYSQL_DATABASE", "farmora"))

source_db = pymysql.connect(
    host=SOURCE_HOST,
    port=SOURCE_PORT,
    user=SOURCE_USER,
    password=SOURCE_PASSWORD,
    database=SOURCE_DATABASE
)

# ============================================
# DESTINATION DATABASE (Loaded from .env / env vars)
# ============================================

DEST_HOST = os.environ.get("DEST_MYSQL_HOST", "database-1.cl84msuko0wj.eu-north-1.rds.amazonaws.com")
DEST_PORT = int(os.environ.get("DEST_MYSQL_PORT", 3306))
DEST_USER = os.environ.get("DEST_MYSQL_USER", "admin")
DEST_PASSWORD = os.environ.get("DEST_MYSQL_PASSWORD", "6Td%T%3DBg")
DEST_DATABASE = os.environ.get("DEST_MYSQL_DATABASE", "farmora")

target_db = pymysql.connect(
    host=DEST_HOST,
    port=DEST_PORT,
    user=DEST_USER,
    password=DEST_PASSWORD,
    database=DEST_DATABASE
)


print("Source Database connected!")
print("Destination Database connected!")


# ============================================
# CURSORS
# ============================================

source_cursor = source_db.cursor()
target_cursor = target_db.cursor()


# ============================================
# TABLES
# ============================================

tables = [
    "Category",
    "Customer_Details",
    "Product",
    "Order_Details",
    "Cart",
    "Wishlist"
]


# ============================================
# BATCH SIZE
# ============================================

BATCH_SIZE = 10000


# ============================================
# DISABLE FOREIGN KEY CHECKS
# ============================================

target_cursor.execute(
    "SET FOREIGN_KEY_CHECKS = 0"
)

print("Foreign key checks disabled")


# ============================================
# COPY EACH TABLE
# ============================================

for table in tables:

    print("\n====================================")
    print("Processing:", table)
    print("====================================")


    # ----------------------------------------
    # 1. TRUNCATE DESTINATION
    # ----------------------------------------

    target_cursor.execute(
        f"TRUNCATE TABLE `{table}`"
    )

    target_db.commit()

    print("Destination table truncated")


    # ----------------------------------------
    # 2. GET COLUMN COUNT
    # ----------------------------------------

    source_cursor.execute(
        f"SELECT * FROM `{table}` LIMIT 0"
    )

    column_count = len(source_cursor.description)


    # ----------------------------------------
    # 3. CREATE INSERT QUERY
    # ----------------------------------------

    placeholders = ", ".join(
        ["%s"] * column_count
    )

    insert_query = f"""
        INSERT INTO `{table}`
        VALUES ({placeholders})
    """


    # ----------------------------------------
    # 4. SELECT ALL DATA FROM SOURCE
    # ----------------------------------------

    source_cursor.execute(
        f"SELECT * FROM `{table}`"
    )


    # ----------------------------------------
    # 5. INSERT IN BATCHES
    # ----------------------------------------

    total_inserted = 0

    while True:

        data = source_cursor.fetchmany(BATCH_SIZE)

        if not data:
            break

        target_cursor.executemany(
            insert_query,
            data
        )

        target_db.commit()

        total_inserted += len(data)

        print(
            f"Inserted {total_inserted} rows into {table}"
        )


    # ----------------------------------------
    # 6. TABLE COMPLETED
    # ----------------------------------------

    print(
        f"Completed {table} - "
        f"Total rows inserted: {total_inserted}"
    )


# ============================================
# ENABLE FOREIGN KEY CHECKS
# ============================================

target_cursor.execute(
    "SET FOREIGN_KEY_CHECKS = 1"
)

target_db.commit()

print("\nForeign key checks enabled")


# ============================================
# CLOSE CONNECTIONS
# ============================================

source_cursor.close()
target_cursor.close()

source_db.close()
target_db.close()


# ============================================
# COMPLETED
# ============================================

print("\n====================================")
print("ALL TABLES COPIED SUCCESSFULLY!")
print("====================================")