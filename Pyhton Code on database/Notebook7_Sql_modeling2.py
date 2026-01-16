import sqlite3
import pandas as pd

conn = sqlite3.connect(r"D:\project\database\database\business.db")
cursor = conn.cursor()

region_segment = pd.read_sql("""
SELECT
    c.Region,
    c.Segment,
    SUM(f.Sales) AS total_sales,
    SUM(f.Profit) AS total_profit,
    ROUND(AVG(f.Profit/f.Sales),2) AS avg_profit_margin
FROM fact_sales f
JOIN dim_customer c
    ON f.customer_id = c.customer_id
GROUP BY c.Region, c.Segment
ORDER BY total_sales DESC;
""", conn)

print(region_segment)

revenue_growth = pd.read_sql("""
WITH monthly_sales AS (
    SELECT
        strftime('%Y-%m', order_date) AS month,
        SUM(Sales) AS revenue
    FROM fact_sales
    GROUP BY month
)
SELECT
    month,
    revenue,
    LAG(revenue) OVER (ORDER BY month) AS prev_month_revenue,
    ROUND((revenue - LAG(revenue) OVER (ORDER BY month)) / LAG(revenue) OVER (ORDER BY month) * 100,2) AS growth_pct
FROM monthly_sales;
""", conn)

print(revenue_growth)

top_customers_profit = pd.read_sql("""
SELECT
    c.customer_id,
    c.customer_name,
    SUM(f.Sales) AS total_sales,
    SUM(f.Profit) AS total_profit,
    ROUND(AVG(f.Profit/f.Sales),2) AS avg_profit_margin
FROM fact_sales f
JOIN dim_customer c
    ON f.customer_id = c.customer_id
GROUP BY c.customer_id
ORDER BY total_profit DESC
LIMIT 10;
""", conn)

print(top_customers_profit)

cohort = pd.read_sql("""
WITH first_order AS (
    SELECT
        customer_id,
        MIN(strftime('%Y-%m', order_date)) AS first_order_month
    FROM fact_sales
    GROUP BY customer_id
),
orders AS (
    SELECT
        f.customer_id,
        strftime('%Y-%m', f.order_date) AS order_month
    FROM fact_sales f
)
SELECT
    f.first_order_month,
    o.order_month,
    COUNT(DISTINCT o.customer_id) AS active_customers
FROM first_order f
JOIN orders o
    ON f.customer_id = o.customer_id
GROUP BY f.first_order_month, o.order_month
ORDER BY f.first_order_month, o.order_month;
""", conn)

print(cohort.head(12))


