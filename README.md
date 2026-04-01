# Uber Eats Bangalore — Restaurant Intelligence (Guvi capstone)

I started this in **Google Colab** (`ubereats_py.ipynb`, `order_json.ipynb`): cleaning the CSV, splitting cuisines for analysis, building a **score** (rating × log(1 + votes)), loading orders from JSON into SQLite. This repo is the same work moved into **scripts + Streamlit** so it is easy to run and submit.

**What you get:** Streamlit app, **tables only** (no charts). Dashboard filters + **15** restaurant questions + **6** order questions, all backed by SQL.

## Data files (same as in Colab)

Put in this folder:

- `Uber_Eats_data.csv`
- `orders.json` (optional — if missing, sample orders are generated so the Orders page still runs)

## Run

```bash
pip install -r requirements.txt
python create_db.py
streamlit run app.py
```

## What I did in code (short)

| Piece | What |
|--------|------|
| `pipeline.py` | Drop `phone` / `listed_in(city)`, **drop duplicate rows**, rename cost columns, build **`cuisine_exploded`** (split cuisines), **`restaurant_scores`** (score for Q15), **`orders`** from JSON + weekday/month from `order_date` |
| `create_db.py` | Creates / refreshes `ubereats.db` |
| `app.py` | Streamlit + SQL; dashboard filters use **parameterised** queries |

## Viva pointers

- **EDA:** row counts before/after dedupe, rating and cost cleaning, cuisine split vs full string.  
- **Stats:** e.g. chi-square (online order vs high/low rating) — explain why.  
- **Q15:** score rewards both rating and vote volume so busy places are not ignored.

Submit the **GitHub repo link** in ZEN as the course asks.
