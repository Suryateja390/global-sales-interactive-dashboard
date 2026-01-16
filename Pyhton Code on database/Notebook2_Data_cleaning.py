import pandas as pd

df = pd.read_excel("D:\project\database\global_superstore_2016.xlsx")

# Missing values
missing = df.isna().sum().sort_values(ascending=False)
print(missing.head(10))


# ---- Fix data types ----
df['Order Date'] = pd.to_datetime(df['Order Date'])

# ---- Handle missing postal code ----
df['Postal Code'] = df['Postal Code'].fillna(0)
df['Postal Code'] = df['Postal Code'].astype(int)

# ---- Create time features ----
df['Order Year'] = df['Order Date'].dt.year
df['Order Month'] = df['Order Date'].dt.month
df['Order Quarter'] = df['Order Date'].dt.to_period('Q').astype(str)

# ---- Create business performance features ----
df['Profit Margin'] = df['Profit'] / df['Sales']
df['Shipping Ratio'] = df['Shipping Cost'] / df['Sales']

# ---- Save clean dataset ----
df.to_csv("D:/project/database/clean_superstore.csv", index=False)

print("Data cleaning & feature engineering completed successfully")
