# Uber Eats Bangalore — Restaurant Intelligence (Guvi capstone)

Streamlit + SQLite: **tables only** (no charts). Dashboard filters, **15** restaurant Q&A queries, **6** order queries.

## Data files (put them in this folder)

Copy from your machine, e.g. Downloads:

- `Uber_Eats_data.csv`
- `orders.json` (list of orders; `order_date` is turned into `day_of_week` and `month` in `pipeline.py` for SQL)

Then:

```bash
pip install -r requirements.txt
python create_db.py
streamlit run app.py
```

## What each main file does

| File | Role |
|------|------|
| `pipeline.py` | ETL: clean CSV → `restaurants`; load JSON → `orders` (+ date fields for analytics) |
| `create_db.py` | Runs the pipeline and builds `ubereats.db` |
| `app.py` | Streamlit UI + SQL (parameterized filters on Dashboard) |

If `orders.json` is missing, the pipeline creates **sample** order rows so the Orders page still runs (explain that in evaluation if you demo without real JSON).

## Viva in one minute

- **Domain:** food-delivery marketplace analytics.  
- **EDA:** rows/columns, missing values, rating and cost cleaning, what you found on locations/cuisines.  
- **Stats:** one test (e.g. chi-square: online order vs high/low rating) + why you picked it.  
- **Business:** 1–2 actions from your tables (e.g. where to onboard partners, price segment insight).

Submit this repo in ZEN as required by the course.
