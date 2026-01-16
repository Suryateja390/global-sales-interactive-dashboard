import sqlite3
import pandas as pd

# Connect to your database
conn = sqlite3.connect(r"D:\project\database\database\business.db")
cursor = conn.cursor()

tables = pd.read_sql("SELECT name FROM sqlite_master WHERE type='table';", conn)
print(tables)

kpi_revenue = pd.read_sql("""
SELECT
    SUM(Sales) AS total_revenue,
    SUM(Profit) AS total_profit,
    ROUND(AVG(Profit/Sales), 2) AS avg_profit_margin
FROM fact_sales;
""", conn)

print(kpi_revenue)

kpi_time = pd.read_sql("""
SELECT
    strftime('%Y', order_date) AS order_year,
    strftime('%m', order_date) AS order_month,
    SUM(Sales) AS revenue,
    SUM(Profit) AS profit
FROM fact_sales
GROUP BY order_year, order_month
ORDER BY order_year, order_month;
""", conn)

print(kpi_time.head(12))

top_customers = pd.read_sql("""
SELECT
    customer_id,
    SUM(Sales) AS total_sales,
    SUM(Profit) AS total_profit
FROM fact_sales
GROUP BY customer_id
ORDER BY total_sales DESC
LIMIT 10;
""", conn)

print(top_customers)

top_products = pd.read_sql("""
SELECT
    product_id,
    SUM(Sales) AS total_sales,
    SUM(Profit) AS total_profit
FROM fact_sales
GROUP BY product_id
ORDER BY total_profit DESC
LIMIT 10;
""", conn)

print(top_products)

customer_churn = pd.read_sql("""
SELECT
    customer_id,
    COUNT(DISTINCT order_id) AS orders_count,
    MAX(order_date) AS last_order_date
FROM fact_sales
GROUP BY customer_id
ORDER BY last_order_date ASC;
""", conn)

print(customer_churn.head(10))

conn.close()
