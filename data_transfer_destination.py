import pymysql


# ============================================
# SOURCE DATABASE
# ============================================

source_db = pymysql.connect(
    host="localhost",
    user="root",
    password="root123",
    database="farmora"
)


# ============================================
# DESTINATION DATABASE
# ============================================

target_db = pymysql.connect(
    host="database-1.cl84msuko0wj.eu-north-1.rds.amazonaws.com",
    user="admin",
    password="6Td%T%3DBg",
    database="farmora"
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