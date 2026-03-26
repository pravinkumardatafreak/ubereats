# ubereats

## Project Status
- ✅ Completed: interactive Streamlit dashboard for Bangalore restaurant and orders intelligence
- ✅ SQLite database connection (`ubereats.db`)
- ✅ Dynamic filters and results for restaurants
- ✅ Q&A analytics with 10 business questions
- ✅ Orders analytics with 6 revenue/discount/payment views

## How to run
1. Install dependencies:
   - `pip install streamlit pandas sqlite3`
2. Make sure `ubereats.db` exists in the project folder (use `create_db.py` if needed)
3. Start the app:
   - `streamlit run app.py`
4. Open in browser:
   - `http://localhost:8501`

## Streamlit report (runtime your local link)
- After `streamlit run app.py`, access `http://localhost:8501` (default)
- If port is in use, Streamlit will show alternative port (`http://localhost:8502`, etc.)

## Quick summary of app features
- Dashboard: location, order/table booking, rating filters with top restaurants data table
- Q&A Analysis: selectable queries for location, cuisine, cost/rating metrics
- Orders Analysis: revenue by payment, discount, day, restaurant, month

> Final note: Project is complete and ready for handoff or demo.

