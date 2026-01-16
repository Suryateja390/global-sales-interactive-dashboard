import sqlite3
import pandas as pd

db_path = r"D:\project\database\database\business.db"
conn = sqlite3.connect(db_path)

tables = ["fact_sales", "dim_customer", "dim_product", "dim_date"]

for table in tables:
    df = pd.read_sql_query(f"SELECT * FROM {table}", conn)
    df.to_csv(f"D:/project/{table}.csv", index=False)

conn.close()
print("Export completed.")
