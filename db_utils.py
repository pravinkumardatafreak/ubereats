"""Database utility module for Uber Eats Bangalore Restaurant Intelligence.

This module encapsulates all sqlite3 connection logic and implements parameterized
SQL queries to protect the application from SQL injection vulnerabilities.
It conforms to standard PEP-8 style practices.
"""

import os
import sqlite3
import pandas as pd


def run_query(query: str, params: tuple = ()) -> pd.DataFrame:
    """Execute a read query securely using parameterized syntax and return a DataFrame.

    This function utilizes python's context manager (the 'with' block) to ensure
    connections are closed immediately and cleanly, avoiding resource leaks.

    Args:
        query (str): The parameterized SQL query string.
        params (tuple): Query parameters to safely inject.

    Returns:
        pd.DataFrame: Query results in DataFrame format.
    """
    db_path = "ubereats.db"
    try:
        with sqlite3.connect(db_path) as conn:
            df = pd.read_sql_query(query, conn, params=params)
            return df
    except sqlite3.Error as e:
        raise RuntimeError(f"Database query failed: {e}") from e


def get_unique_locations() -> list:
    """Retrieve the sorted list of distinct locations.

    Returns:
        list: Sorted unique locations as strings.
    """
    query = "SELECT DISTINCT location FROM restaurants ORDER BY location"
    try:
        df = run_query(query)
        return df["location"].dropna().tolist()
    except Exception:
        return []


def get_filtered_restaurants(
    min_rating: float,
    location: str = "All",
    online_order: str = "All",
    book_table: str = "All",
    search_name: str = "",
) -> pd.DataFrame:
    """Query restaurants applying filters securely via parameterized arguments.

    Args:
        min_rating (float): Lower bound rating value (e.g. 3.0).
        location (str): Selected location or 'All'.
        online_order (str): Selected online delivery option or 'All'.
        book_table (str): Selected table booking option or 'All'.
        search_name (str): Substring to search restaurant names (optional).

    Returns:
        pd.DataFrame: Cleaned and filtered DataFrame.
    """
    query = """
        SELECT DISTINCT name, location, cuisines, rate, 
               votes, online_order, book_table,
               approx_cost_fortwo, restaurant_type
        FROM restaurants
        WHERE rate >= ?
    """
    params = [min_rating]

    if location != "All":
        query += " AND location = ?"
        params.append(location)

    if online_order != "All":
        query += " AND online_order = ?"
        params.append(online_order)

    if book_table != "All":
        query += " AND book_table = ?"
        params.append(book_table)

    if search_name.strip():
        query += " AND name LIKE ?"
        params.append(f"%{search_name.strip()}%")

    query += " ORDER BY rate DESC"

    return run_query(query, tuple(params))


def check_db_integrity() -> bool:
    """Check if the database and its critical tables exist.

    If not found, returns False so the caller can trigger creation.
    """
    if not os.path.exists("ubereats.db"):
        return False
    try:
        # Check if 'restaurants' table exists and contains columns
        df = run_query("SELECT name FROM sqlite_master WHERE type='table' AND name='restaurants'")
        return not df.empty
    except Exception:
        return False
