"""Build SQLite DB from CSV (and optional orders JSON). Run: python create_db.py"""
from pipeline import build_database

if __name__ == "__main__":
    build_database()
    print("Clean database created successfully (restaurants + orders).")
