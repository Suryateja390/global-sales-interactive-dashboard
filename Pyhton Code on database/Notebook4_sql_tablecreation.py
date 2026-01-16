import sqlite3

conn = sqlite3.connect(r"D:\project\Database\database\business.db")
cursor = conn.cursor()

# ===============================
# CUSTOMER DIMENSION
# ===============================
cursor.execute("""
CREATE TABLE IF NOT EXISTS dim_customer AS
SELECT DISTINCT
    "Customer ID" AS customer_id,
    "Customer Name" AS customer_name,
    Segment,
    Country,
    City,
    State,
    "Postal Code",
    Region
FROM raw_sales;
""")

# ===============================
# PRODUCT DIMENSION
# ===============================
cursor.execute("""
CREATE TABLE IF NOT EXISTS dim_product AS
SELECT DISTINCT
    "Product ID" AS product_id,
    Category,
    "Sub-Category" AS sub_category,
    "Product Name" AS product_name
FROM raw_sales;
""")

# ===============================
# DATE DIMENSION
# ===============================
cursor.execute("""
CREATE TABLE IF NOT EXISTS dim_date AS
SELECT DISTINCT
    "Order Date" AS order_date
FROM raw_sales;
""")

# ===============================
# FACT TABLE
# ===============================
cursor.execute("""
CREATE TABLE IF NOT EXISTS fact_sales AS
SELECT
    "Order ID" AS order_id,
    "Order Date" AS order_date,
    "Customer ID" AS customer_id,
    "Product ID" AS product_id,
    Sales,
    Quantity,
    Discount,
    Profit,
    "Shipping Cost" AS shipping_cost
FROM raw_sales;
""")

conn.commit()
conn.close()

print("Star Schema created successfully")
