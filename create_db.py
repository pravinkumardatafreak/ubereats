import pandas as pd
import sqlite3

# load your cleaned dataset
df = pd.read_csv("Uber_Eats_data.csv")

conn = sqlite3.connect("ubereats.db")

df.to_sql("restaurants", conn, if_exists="replace", index=False)

conn.close()

print("Database created successfully!")