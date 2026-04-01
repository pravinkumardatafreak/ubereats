# Run once after you add Uber_Eats_data.csv (and orders.json if you have it).
from pipeline import build_database

if __name__ == "__main__":
    build_database()
    print("Done: ubereats.db updated (restaurants, cuisine_exploded, restaurant_scores, orders).")
