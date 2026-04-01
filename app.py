import os
import sqlite3

import pandas as pd
import streamlit as st

from pipeline import DEFAULT_CSV, DEFAULT_DB, ensure_database

# ============================================
# DATABASE CONNECTION / SETUP
# ============================================
if os.path.isfile(DEFAULT_CSV):
    ensure_database()
elif not os.path.isfile(DEFAULT_DB):
    st.error(
        "Uber_Eats_data.csv is missing. Add it to the app folder or run create_db.py "
        "after restoring the dataset."
    )
    st.stop()

if not os.path.isfile(DEFAULT_DB):
    st.error("Database could not be initialized.")
    st.stop()

conn = sqlite3.connect(DEFAULT_DB)

# ============================================
# SIDEBAR NAVIGATION
# ============================================
st.sidebar.title("🍽️ Uber Eats Bangalore")
page = st.sidebar.selectbox(
    "📌 Navigate",
    ["🏠 Dashboard", "❓ Q&A Analysis", "📦 Orders Analysis"]
)

# ============================================
# PAGE 1 - DASHBOARD
# ============================================
if page == "🏠 Dashboard":
    st.title("🏠 Restaurant Intelligence Dashboard")
    st.markdown("Filter restaurants dynamically using SQL!")
    
    # --- FILTERS ---
    col1, col2 = st.columns(2)
    
    with col1:
        # Location filter
        locations = pd.read_sql_query(
            "SELECT DISTINCT location FROM restaurants ORDER BY location", 
            conn
        )
        selected_location = st.selectbox(
            "📍 Location", 
            ["All"] + locations['location'].tolist()
        )
        
        # Online order filter
        selected_online = st.selectbox(
            "🛵 Online Order", 
            ["All", "Yes", "No"]
        )
    
    with col2:
        # Book table filter
        selected_booking = st.selectbox(
            "🪑 Book Table", 
            ["All", "Yes", "No"]
        )
        
        # Rating filter
        selected_rate = st.slider(
            "⭐ Minimum Rating", 
            min_value=1.0, 
            max_value=5.0, 
            value=3.0, 
            step=0.1
        )
    
    # --- BUILD SQL (parameterized) ---
    clauses = ["rate >= ?"]
    params: list = [selected_rate]
    if selected_location != "All":
        clauses.append("location = ?")
        params.append(selected_location)
    if selected_online != "All":
        clauses.append("online_order = ?")
        params.append(selected_online)
    if selected_booking != "All":
        clauses.append("book_table = ?")
        params.append(selected_booking)
    query = """
        SELECT name, location, cuisines, rate,
               votes, online_order, book_table,
               approx_cost_fortwo, restaurant_type
        FROM restaurants
        WHERE """ + " AND ".join(
        clauses
    ) + """
        ORDER BY rate DESC
    """
    df_filtered = pd.read_sql_query(query, conn, params=params)
    st.markdown(f"### 📊 Results: {len(df_filtered)} restaurants found")
    st.dataframe(df_filtered)

# ============================================
# PAGE 2 - Q&A
# ============================================
elif page == "❓ Q&A Analysis":
    st.title("❓ Business Intelligence Q&A")
    
    question = st.selectbox("Select Question", [
        "Q1 - Top Rated Locations",
        "Q2 - Over Saturated Locations",
        "Q3 - Online Ordering Impact",
        "Q4 - Table Booking Impact",
        "Q5 - Best Price Range",
        "Q6 - Price Segment Performance",
        "Q7 - Most Common Cuisines",
        "Q8 - Highest Rated Cuisines",
        "Q9 - Niche Cuisine Opportunities",
        "Q10 - Cost vs Rating",
        "Q11 - Premium Onboarding Locations",
        "Q12 - High Demand Low Rating Areas",
        "Q13 - Online + Table Booking Bundle",
        "Q14 - Multi-Factor Location Success",
        "Q15 - Top Restaurants by Price Segment",
    ])
    
    queries = {
        "Q1 - Top Rated Locations": """
            SELECT location, ROUND(AVG(rate),2) as avg_rating,
            COUNT(name) as total_restaurants
            FROM restaurants
            GROUP BY location
            ORDER BY avg_rating DESC LIMIT 10
        """,
        "Q2 - Over Saturated Locations": """
            SELECT location, COUNT(name) as total_restaurants
            FROM restaurants
            GROUP BY location
            ORDER BY total_restaurants DESC LIMIT 10
        """,
        "Q3 - Online Ordering Impact": """
            SELECT online_order, ROUND(AVG(rate),2) as avg_rating,
            COUNT(name) as total_restaurants
            FROM restaurants GROUP BY online_order
        """,
        "Q4 - Table Booking Impact": """
            SELECT book_table, ROUND(AVG(rate),2) as avg_rating,
            COUNT(name) as total_restaurants
            FROM restaurants GROUP BY book_table
        """,
        "Q5 - Best Price Range": """
            SELECT CASE 
                WHEN approx_cost_fortwo < 500 THEN 'Low'
                WHEN approx_cost_fortwo BETWEEN 500 AND 800 THEN 'Mid'
                ELSE 'Premium' END as price_segment,
            ROUND(AVG(rate),2) as avg_rating
            FROM restaurants
            GROUP BY price_segment
            ORDER BY avg_rating DESC LIMIT 1
        """,
        "Q6 - Price Segment Performance": """
            SELECT CASE 
                WHEN approx_cost_fortwo < 500 THEN 'Low'
                WHEN approx_cost_fortwo BETWEEN 500 AND 800 THEN 'Mid'
                ELSE 'Premium' END as price_segment,
            ROUND(AVG(rate),2) as avg_rating,
            COUNT(name) as total_restaurants
            FROM restaurants
            GROUP BY price_segment
            ORDER BY avg_rating DESC
        """,
        "Q7 - Most Common Cuisines": """
            SELECT cuisines, COUNT(name) as total_restaurants
            FROM restaurants
            GROUP BY cuisines
            ORDER BY total_restaurants DESC LIMIT 10
        """,
        "Q8 - Highest Rated Cuisines": """
            SELECT cuisines, ROUND(AVG(rate),2) as avg_rating
            FROM restaurants
            GROUP BY cuisines
            ORDER BY avg_rating DESC LIMIT 10
        """,
        "Q9 - Niche Cuisine Opportunities": """
            SELECT cuisines, ROUND(AVG(rate),2) as avg_rating,
            COUNT(name) as total_restaurants
            FROM restaurants
            GROUP BY cuisines
            HAVING AVG(rate) > 4.0 AND COUNT(name) < 10
            ORDER BY avg_rating DESC LIMIT 10
        """,
        "Q10 - Cost vs Rating": """
            SELECT CASE 
                WHEN approx_cost_fortwo < 500 THEN 'Low'
                WHEN approx_cost_fortwo BETWEEN 500 AND 800 THEN 'Mid'
                ELSE 'Premium' END as cost_category,
            ROUND(AVG(rate),2) as avg_rating,
            ROUND(AVG(approx_cost_fortwo),2) as avg_cost
            FROM restaurants
            GROUP BY cost_category
            ORDER BY avg_cost ASC
        """,
        "Q11 - Premium Onboarding Locations": """
            SELECT location,
                ROUND(AVG(rate),2) as avg_rating,
                ROUND(AVG(approx_cost_fortwo),2) as avg_cost,
                COUNT(name) as restaurant_count
            FROM restaurants
            WHERE approx_cost_fortwo >= 700
            GROUP BY location
            HAVING COUNT(name) >= 3 AND AVG(rate) >= 4.0
            ORDER BY avg_rating DESC, avg_cost DESC
            LIMIT 15
        """,
        "Q12 - High Demand Low Rating Areas": """
            WITH agg AS (
                SELECT location, COUNT(name) AS cnt, AVG(rate) AS avg_r
                FROM restaurants GROUP BY location
            )
            SELECT location, cnt AS total_restaurants,
                ROUND(avg_r, 2) AS avg_rating
            FROM agg
            WHERE cnt > (SELECT AVG(cnt) FROM agg)
              AND avg_r < (SELECT AVG(rate) FROM restaurants)
            ORDER BY cnt DESC
            LIMIT 15
        """,
        "Q13 - Online + Table Booking Bundle": """
            SELECT CASE
                WHEN online_order = 'Yes' AND book_table = 'Yes' THEN 'Both Yes'
                ELSE 'Other'
            END AS segment,
            ROUND(AVG(rate),2) AS avg_rating,
            COUNT(*) AS total_restaurants
            FROM restaurants
            GROUP BY segment
        """,
        "Q14 - Multi-Factor Location Success": """
            SELECT location,
                ROUND(AVG(rate),2) AS avg_rating,
                ROUND(AVG(approx_cost_fortwo),2) AS avg_cost,
                ROUND(100.0 * SUM(CASE WHEN online_order = 'Yes' THEN 1 ELSE 0 END) / COUNT(*), 1) AS pct_online,
                ROUND(100.0 * SUM(CASE WHEN book_table = 'Yes' THEN 1 ELSE 0 END) / COUNT(*), 1) AS pct_book_table,
                COUNT(name) AS restaurants
            FROM restaurants
            GROUP BY location
            HAVING COUNT(name) >= 5
            ORDER BY avg_rating DESC, pct_online DESC
            LIMIT 15
        """,
        "Q15 - Top Restaurants by Price Segment": """
            WITH r AS (
                SELECT name, location,
                    CASE
                        WHEN approx_cost_fortwo < 500 THEN 'Low'
                        WHEN approx_cost_fortwo BETWEEN 500 AND 800 THEN 'Mid'
                        ELSE 'Premium'
                    END AS price_segment,
                    rate,
                    ROW_NUMBER() OVER (
                        PARTITION BY CASE
                            WHEN approx_cost_fortwo < 500 THEN 'Low'
                            WHEN approx_cost_fortwo BETWEEN 500 AND 800 THEN 'Mid'
                            ELSE 'Premium'
                        END
                        ORDER BY rate DESC
                    ) AS rn
                FROM restaurants
            )
            SELECT name, location, price_segment, rate
            FROM r WHERE rn <= 5
            ORDER BY price_segment, rate DESC
        """,
    }
    
    if st.button("🔍 Run Analysis"):
        df_result = pd.read_sql_query(queries[question], conn)
        st.dataframe(df_result)

# ============================================
# PAGE 3 - ORDERS
# ============================================
elif page == "📦 Orders Analysis":
    st.title("📦 Orders Intelligence")
    
    order_question = st.selectbox("Select Question", [
        "OQ1 - Payment Method Revenue",
        "OQ2 - Discount Impact",
        "OQ3 - Revenue by Day",
        "OQ4 - Top Restaurants by Revenue",
        "OQ5 - Monthly Revenue",
        "OQ6 - Payment + Discount Combined"
    ])
    
    order_queries = {
        "OQ1 - Payment Method Revenue": """
            SELECT payment_method, COUNT(*) as total_orders,
            ROUND(SUM(order_value),2) as total_revenue
            FROM orders GROUP BY payment_method
            ORDER BY total_revenue DESC
        """,
        "OQ2 - Discount Impact": """
            SELECT discount_used, COUNT(*) as total_orders,
            ROUND(AVG(order_value),2) as avg_order_value
            FROM orders GROUP BY discount_used
        """,
        "OQ3 - Revenue by Day": """
            SELECT day_of_week, COUNT(*) as total_orders,
            ROUND(SUM(order_value),2) as total_revenue
            FROM orders GROUP BY day_of_week
            ORDER BY total_revenue DESC
        """,
        "OQ4 - Top Restaurants by Revenue": """
            SELECT restaurant_name, COUNT(*) as total_orders,
            ROUND(SUM(order_value),2) as total_revenue
            FROM orders GROUP BY restaurant_name
            ORDER BY total_revenue DESC LIMIT 10
        """,
        "OQ5 - Monthly Revenue": """
            SELECT month, COUNT(*) as total_orders,
            ROUND(SUM(order_value),2) as total_revenue
            FROM orders GROUP BY month
            ORDER BY total_revenue DESC
        """,
        "OQ6 - Payment + Discount Combined": """
            SELECT payment_method, discount_used,
            COUNT(*) as total_orders,
            ROUND(SUM(order_value),2) as total_revenue
            FROM orders GROUP BY payment_method, discount_used
            ORDER BY total_revenue DESC
        """
    }
    
    if st.button("🔍 Run Analysis"):
        df_result = pd.read_sql_query(order_queries[order_question], conn)
        st.dataframe(df_result)