import pandas as pd
import sqlite3

df = pd.read_excel(r"D:\project\Database\global_superstore_2016.xlsx")

conn = sqlite3.connect(r"D:\project\Database\database\business.db")

df.to_sql("raw_sales", conn, if_exists="replace", index=False)

print("Database created successfully")
