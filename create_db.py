# create_db.py - Fixed version (no dependency on missing pipeline.py)

import pandas as pd
import sqlite3
import os

def clean_restaurants(df: pd.DataFrame) -> pd.DataFrame:
    """Clean + rename columns properly."""
    df = df.copy()

    # Clean rate
    df["rate"] = df["rate"].astype(str).str.replace("/5", "", regex=False)
    df["rate"] = pd.to_numeric(df["rate"], errors="coerce")
    df = df[df["rate"].notnull()].reset_index(drop=True)

    # Clean cost
    cost_col = "approx_cost(for two people)"
    if cost_col in df.columns:
        df[cost_col] = df[cost_col].astype(str).str.replace(",", "", regex=False)
        df[cost_col] = pd.to_numeric(df[cost_col], errors="coerce")

    # Drop unnecessary columns
    for col in ("phone", "listed_in(city)"):
        if col in df.columns:
            df = df.drop(columns=[col])

    # Deduplicate (important for dashboard)
    subset_cols = ['name', 'location', 'cuisines', 'rate', cost_col]
    df = df.drop_duplicates(subset=subset_cols, keep='first').reset_index(drop=True)

    # Rename columns
    df.rename(columns={
        "approx_cost(for two people)": "approx_cost_fortwo",
        "listed_in(type)": "restaurant_type",
    }, inplace=True)

    return df

# ===================== MAIN =====================
if __name__ == "__main__":
    csv_path = "Uber_Eats_data.csv"
    db_path = "ubereats.db"

    if not os.path.isfile(csv_path):
        print("Error: Uber_Eats_data.csv not found!")
    else:
        print("Loading and cleaning data...")
        df = pd.read_csv(csv_path)
        df = clean_restaurants(df)

        # Build database
        conn = sqlite3.connect(db_path)
        
        df.to_sql("restaurants", conn, if_exists="replace", index=False)
        print(f"✓ restaurants table created with {len(df)} rows")
        print("Columns:", df.columns.tolist())

        # Simple orders table (if orders.json exists)
        if os.path.isfile("orders.json"):
            import json
            with open("orders.json") as f:
                orders_data = json.load(f)
            orders_df = pd.DataFrame(orders_data)
            orders_df.to_sql("orders", conn, if_exists="replace", index=False)
            print("✓ orders table created")

        conn.close()
        print("\n✅ Done! ubereats.db has been rebuilt with correct column names.")