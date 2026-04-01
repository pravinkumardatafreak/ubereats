import pandas as pd
import sqlite3
# 1. LOAD DATA
df = pd.read_csv("Uber_Eats_data.csv")
# 2. CLEAN 'rate' COLUMN
# Remove '/5'
df['rate'] = df['rate'].astype(str).str.replace('/5', '', regex=False)

# Convert to numeric safely (invalid → NaN)
df['rate'] = pd.to_numeric(df['rate'], errors='coerce')

# Drop corrupted/missing ratings
df = df[df['rate'].notnull()]
# 3. CLEAN 'approx_cost(for two people)'
df['approx_cost(for two people)'] = df['approx_cost(for two people)'] \
    .astype(str).str.replace(',', '', regex=False)

df['approx_cost(for two people)'] = pd.to_numeric(
    df['approx_cost(for two people)'], errors='coerce'
)

# 4. RENAME COLUMNS (VERY IMPORTANT)
df.rename(columns={
    'approx_cost(for two people)': 'approx_cost_fortwo',
    'listed_in(type)': 'restaurant_type',
    'listed_in(city)': 'city'
}, inplace=True)

# 5. CREATE DATABASE
conn = sqlite3.connect("ubereats.db")

df.to_sql("restaurants", conn, if_exists="replace", index=False)

conn.close()

print("Clean database created successfully!")
