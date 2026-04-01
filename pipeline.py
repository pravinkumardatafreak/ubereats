# ETL for Uber Eats capstone — builds SQLite tables used by create_db.py and Streamlit.
# Cleaning + cuisine split + score table follow what I prototyped in ubereats_py.ipynb (Colab).

from __future__ import annotations

import json
import os
import sqlite3
from typing import Optional

import numpy as np
import pandas as pd

DEFAULT_CSV = "Uber_Eats_data.csv"
DEFAULT_DB = "ubereats.db"
ORDER_JSON_CANDIDATES = ("orders.json", "Order_json.json", "order_data.json")


def clean_restaurants(df: pd.DataFrame) -> pd.DataFrame:
    """Same steps as my notebook: fix rate/cost, drop unused cols, remove duplicate rows."""
    df = df.copy()
    df["rate"] = df["rate"].astype(str).str.replace("/5", "", regex=False)
    df["rate"] = pd.to_numeric(df["rate"], errors="coerce")
    df = df[df["rate"].notnull()]

    cost_col = "approx_cost(for two people)"
    df[cost_col] = df[cost_col].astype(str).str.replace(",", "", regex=False)
    df[cost_col] = pd.to_numeric(df[cost_col], errors="coerce")

    # Not needed for SQL questions — dropped these in Colab too
    for col in ("phone", "listed_in(city)"):
        if col in df.columns:
            df = df.drop(columns=[col])

    df = df.drop_duplicates(keep="first")

    df.rename(
        columns={
            "approx_cost(for two people)": "approx_cost_fortwo",
            "listed_in(type)": "restaurant_type",
        },
        inplace=True,
    )
    return df


def build_cuisine_exploded(df: pd.DataFrame) -> pd.DataFrame:
    """Split comma-separated cuisines (one row per cuisine tag) — used for Q7–Q9 in SQL."""
    base = df.dropna(subset=["cuisines"]).copy()
    out = base.assign(cuisine=base["cuisines"].str.split(",")).explode("cuisine")
    out["cuisine"] = out["cuisine"].str.strip()
    out = out[out["cuisine"].astype(str).str.len() > 0]
    return out[["cuisine", "name", "location", "rate"]]


def build_restaurant_scores(df: pd.DataFrame) -> pd.DataFrame:
    """score = avg_rating * log(1 + total_votes) — my Q15 logic from the notebook."""
    g = df.groupby(["name", "location", "cuisines", "approx_cost_fortwo"], as_index=False).agg(
        avg_rating=("rate", "mean"),
        total_votes=("votes", "sum"),
    )
    g = g[g["total_votes"] > 50]
    g["score"] = np.round(g["avg_rating"] * np.log1p(g["total_votes"]), 2)
    return g


def _find_orders_json() -> Optional[str]:
    for name in ORDER_JSON_CANDIDATES:
        if os.path.isfile(name):
            return name
    return None


def _enrich_orders_columns(df: pd.DataFrame) -> pd.DataFrame:
    if df.empty or "order_date" not in df.columns:
        return df
    out = df.copy()
    dt = pd.to_datetime(out["order_date"], errors="coerce")
    out["day_of_week"] = dt.dt.day_name()
    # short month label (Jan, Feb) — matches order_json.ipynb style after I standardised
    out["month"] = dt.dt.strftime("%b")
    return out


def load_orders_df(restaurant_names: pd.Series) -> pd.DataFrame:
    path = _find_orders_json()
    if path:
        with open(path, "r", encoding="utf-8") as f:
            raw = json.load(f)
        if isinstance(raw, list):
            df = pd.DataFrame(raw)
        elif isinstance(raw, dict) and "orders" in raw:
            df = pd.DataFrame(raw["orders"])
        else:
            df = pd.DataFrame(raw)
        return _enrich_orders_columns(df)

    rng = np.random.default_rng(42)
    names = restaurant_names.dropna().unique()
    if len(names) == 0:
        return pd.DataFrame(
            columns=[
                "restaurant_name",
                "order_value",
                "payment_method",
                "discount_used",
                "day_of_week",
                "month",
            ]
        )
    n = min(8000, max(2000, len(names) * 20))
    days = [
        "Monday",
        "Tuesday",
        "Wednesday",
        "Thursday",
        "Friday",
        "Saturday",
        "Sunday",
    ]
    months = [
        "Jan",
        "Feb",
        "Mar",
        "Apr",
        "May",
        "Jun",
        "Jul",
        "Aug",
        "Sep",
        "Oct",
        "Nov",
        "Dec",
    ]
    payments = ["UPI", "Card", "Cash", "Wallet"]
    return pd.DataFrame(
        {
            "restaurant_name": rng.choice(names, size=n),
            "order_value": np.round(rng.uniform(150, 1400, size=n), 2),
            "payment_method": rng.choice(payments, size=n),
            "discount_used": rng.choice(["Yes", "No"], size=n),
            "day_of_week": rng.choice(days, size=n),
            "month": rng.choice(months, size=n),
        }
    )


REQUIRED_TABLES = frozenset(
    {"restaurants", "orders", "cuisine_exploded", "restaurant_scores"}
)


def build_database(csv_path: str = DEFAULT_CSV, db_path: str = DEFAULT_DB) -> None:
    if not os.path.isfile(csv_path):
        raise FileNotFoundError(f"Missing dataset: {csv_path}")

    df = pd.read_csv(csv_path)
    df = clean_restaurants(df)

    cuisine_x = build_cuisine_exploded(df)
    scores = build_restaurant_scores(df)

    conn = sqlite3.connect(db_path)
    df.to_sql("restaurants", conn, if_exists="replace", index=False)
    cuisine_x.to_sql("cuisine_exploded", conn, if_exists="replace", index=False)
    scores.to_sql("restaurant_scores", conn, if_exists="replace", index=False)

    orders = load_orders_df(df["name"])
    orders.to_sql("orders", conn, if_exists="replace", index=False)
    conn.close()


def ensure_database(csv_path: str = DEFAULT_CSV, db_path: str = DEFAULT_DB) -> None:
    if not os.path.isfile(csv_path):
        return

    need_full = not os.path.isfile(db_path)
    if not need_full:
        conn = sqlite3.connect(db_path)
        cur = conn.cursor()
        cur.execute("SELECT name FROM sqlite_master WHERE type='table'")
        found = {row[0] for row in cur.fetchall()}
        conn.close()
        need_full = not REQUIRED_TABLES.issubset(found)

    if need_full:
        build_database(csv_path=csv_path, db_path=db_path)
