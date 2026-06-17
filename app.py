"""Streamlit Application for Uber Eats Bangalore Restaurant Intelligence.

This dashboard provides business insights and decision support systems for
restaurateurs and platform analysts. It is designed to be secure (protecting against
SQL injection), modular, and highly visual.
"""

import os
import sqlite3
import json
import pandas as pd
import streamlit as st

import db_utils
import visualization_utils as vu

# ============================================
# APP CONFIGURATION & STYLING
# ============================================
st.set_page_config(
    page_title="Uber Eats Bangalore Intelligence",
    page_icon="🍽️",
    layout="wide",
)

# Premium Custom CSS Injection for a high-end UI/UX experience
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;800&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Outfit', sans-serif;
    }
    
    /* Elegant metric card styling with green accent */
    div[data-testid="stMetric"] {
        background-color: #F8F9FA;
        border-left: 5px solid #06C167;
        padding: 15px;
        border-radius: 6px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    
    div[data-testid="stMetricValue"] {
        font-size: 28px;
        font-weight: 800;
        color: #1F1F1F;
    }
    
    div[data-testid="stMetricLabel"] {
        font-size: 13px;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        color: #7F8C8D;
    }
    
    /* Styled header banners */
    .header-banner {
        background: linear-gradient(135deg, #06C167 0%, #049A51 100%);
        padding: 25px;
        border-radius: 12px;
        color: white;
        margin-bottom: 25px;
        box-shadow: 0 4px 15px rgba(6, 193, 103, 0.2);
    }
    .header-banner h1 {
        margin: 0;
        font-size: 32px;
        font-weight: 800;
    }
    .header-banner p {
        margin: 5px 0 0 0;
        opacity: 0.9;
        font-size: 16px;
    }
    
    /* Custom divider line styling */
    hr {
        margin: 25px 0px;
        border: 0;
        height: 1px;
        background-image: linear-gradient(to right, rgba(0, 0, 0, 0), rgba(6, 193, 103, 0.5), rgba(0, 0, 0, 0));
    }
    
    /* Custom Button styling with micro-animations */
    div.stButton > button {
        background: linear-gradient(135deg, #06C167 0%, #049A51 100%) !important;
        color: white !important;
        font-weight: 700 !important;
        border: none !important;
        padding: 10px 32px !important;
        border-radius: 8px !important;
        box-shadow: 0 4px 12px rgba(6, 193, 103, 0.25) !important;
        transition: all 0.3s ease !important;
        font-size: 15px !important;
    }
    div.stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 18px rgba(6, 193, 103, 0.4) !important;
        background: linear-gradient(135deg, #08D673 0%, #05AA5A 100%) !important;
    }
    div.stButton > button:active {
        transform: translateY(1px) !important;
        box-shadow: 0 2px 6px rgba(6, 193, 103, 0.2) !important;
    }
    
    /* Interactive card styling for Checkboxes */
    div[data-testid="stCheckbox"] {
        background-color: #F8F9FA;
        padding: 12px 18px;
        border-radius: 8px;
        border: 1px solid #E0E0E0;
        transition: all 0.3s ease;
        box-shadow: 0 1px 3px rgba(0,0,0,0.02);
    }
    div[data-testid="stCheckbox"]:hover {
        border-color: #06C167;
        background-color: #F0FAF5;
        box-shadow: 0 3px 10px rgba(6, 193, 103, 0.08);
    }
    div[data-testid="stCheckbox"] label {
        font-weight: 600 !important;
        color: #2C3E50 !important;
    }
    
    /* Ensure st.image aligns center in columns */
    div.stImage > img {
        display: block;
        margin-left: auto;
        margin-right: auto;
        border-radius: 8px;
    }
    
    /* Custom Selectbox & Text Input field focus borders */
    div[data-baseweb="select"], div[data-baseweb="input"] {
        border-radius: 8px !important;
        transition: all 0.3s ease !important;
    }
    
    /* Custom sidebar card menu transitions */
    section[data-testid="stSidebar"] {
        background-image: linear-gradient(180deg, #F0FBF5 0%, #FFFFFF 100%) !important;
        border-right: 1px solid #E2E8F0 !important;
    }
    
    /* Elegant radio items structured as selector cards */
    div[role="radiogroup"] {
        display: flex !important;
        flex-direction: column !important;
        gap: 6px !important;
    }
    div[role="radiogroup"] label {
        background-color: #FFFFFF !important;
        border: 1px solid #E2E8F0 !important;
        padding: 12px 16px !important;
        border-radius: 8px !important;
        transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1) !important;
        box-shadow: 0 1px 3px rgba(0,0,0,0.02) !important;
        cursor: pointer !important;
        border-left: 4px solid transparent !important;
    }
    div[role="radiogroup"] label:hover {
        border-color: #06C167 !important;
        background-color: #F8FFF9 !important;
        box-shadow: 0 4px 12px rgba(6, 193, 103, 0.1) !important;
        transform: translateX(4px) !important;
    }
    div[role="radiogroup"] label:has(input:checked) {
        background-color: #E6F7ED !important;
        border-color: #06C167 !important;
        border-left: 4px solid #06C167 !important;
        font-weight: 600 !important;
        box-shadow: 0 4px 12px rgba(6, 193, 103, 0.15) !important;
    }
    /* Hide circular default pointers for button layout style */
    div[role="radiogroup"] label [data-testid="stVisualCheckbox"] {
        display: none !important;
    }
    
    /* Security glowing badge style */
    .security-card {
        background: linear-gradient(135deg, #1A252C 0%, #0F161A 100%) !important;
        color: #E2E8F0 !important;
        padding: 16px !important;
        border-radius: 10px !important;
        border: 1px solid #28373E !important;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2) !important;
        margin-top: 15px !important;
        transition: all 0.3s ease !important;
    }
    .security-card:hover {
        box-shadow: 0 6px 20px rgba(6, 193, 103, 0.15) !important;
        border-color: #06C167 !important;
    }
    .security-header {
        font-weight: 800 !important;
        font-size: 13px !important;
        color: #06C167 !important;
        text-transform: uppercase !important;
        letter-spacing: 0.6px !important;
        margin-bottom: 12px !important;
        display: flex !important;
        align-items: center !important;
        gap: 8px !important;
    }
    .security-item {
        font-size: 12px !important;
        margin-bottom: 8px !important;
        display: flex !important;
        align-items: center !important;
        gap: 8px !important;
        color: #B0BFC6 !important;
    }
    .check-mark {
        color: #06C167 !important;
        font-weight: 800 !important;
    }
    
    /* Info container styling */
    .insight-box {
        background-color: #E8F8F5;
        border-left: 5px solid #1abc9c;
        padding: 15px;
        border-radius: 6px;
        margin-top: 15px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# ============================================
# DATABASE AUTOPILOT / INITIALIZATION
# ============================================
def ensure_database_exists():
    """Build and clean the database if missing."""
    if not db_utils.check_db_integrity():
        st.warning("Database or tables missing. Building from raw source files...")

        # Build restaurants table
        if os.path.exists("Uber_Eats_data.csv"):
            try:
                import create_db

                df = pd.read_csv("Uber_Eats_data.csv")
                df_clean = create_db.clean_restaurants(df)

                conn = sqlite3.connect("ubereats.db")
                df_clean.to_sql("restaurants", conn, if_exists="replace", index=False)

                # Build orders table
                if os.path.exists("orders.json"):
                    with open("orders.json", "r") as f:
                        orders_data = json.load(f)
                    orders_df = pd.DataFrame(orders_data)
                    orders_df.to_sql("orders", conn, if_exists="replace", index=False)
                    st.success("✓ Database successfully initialized with restaurant and order records!")
                else:
                    st.warning("Database created, but orders.json was missing (orders table skipped).")

                conn.close()
            except Exception as e:
                st.error(f"Error rebuilding database: {e}")
                st.stop()
        else:
            st.error("Uber_Eats_data.csv not found. Please verify the source file.")
            st.stop()


ensure_database_exists()

# ============================================
# SIDEBAR NAVIGATION
# ============================================
st.sidebar.markdown(
    "<h2 style='text-align: center; color: #06C167; font-weight: 800; font-size: 26px; margin-bottom: 2px;'>🍽️ Uber Eats</h2>"
    "<p style='text-align: center; font-size: 12px; color: #7F8C8D; text-transform: uppercase; letter-spacing: 1px; font-weight: 600; margin-top: 0;'>Bangalore Analytics</p>",
    unsafe_allow_html=True,
)
st.sidebar.markdown("---")

page = st.sidebar.radio(
    "📍 SELECT ANALYTICS PAGE",
    ["🏠 Restaurant Search", "❓ Business Q&A Hub", "📦 Orders Intelligence"],
)

st.sidebar.markdown("---")

# Styled security status card in the sidebar
st.sidebar.markdown(
    """
    <div class="security-card">
        <div class="security-header">
            <span class="security-icon">🛡️</span>
            <span>Security Protocol Active</span>
        </div>
        <div class="security-item"><span class="check-mark">✓</span> Input Sanitization: Enabled</div>
        <div class="security-item"><span class="check-mark">✓</span> Query Parameterization: Active</div>
        <div class="security-item"><span class="check-mark">✓</span> Connection Pooling: Managed</div>
    </div>
    """,
    unsafe_allow_html=True,
)

# ============================================
# PAGE 1 - DYNAMIC SEARCH & FILTERS
# ============================================
if page == "🏠 Restaurant Search":
    if os.path.exists("assets/food_dashboard_banner.png"):
        st.image("assets/food_dashboard_banner.png", use_container_width=True)
    
    st.markdown("## 🏠 Restaurant Intelligence Dashboard")
    st.markdown("Filter and query Bangalore restaurants dynamically with parameterized SQL safety.")

    # Search Bar & Main Filters
    col_search, col_loc = st.columns([2, 1])
    with col_search:
        search_name = st.text_input(
            "🔍 Search Restaurant Name (Safe Parameterized Search)",
            placeholder="e.g. Pizza, Cafe, Biryani...",
        )
    with col_loc:
        locations_list = db_utils.get_unique_locations()
        selected_location = st.selectbox("📍 Location", ["All"] + locations_list)

    col_filters = st.columns(3)
    with col_filters[0]:
        selected_online = st.selectbox("🛵 Online Ordering", ["All", "Yes", "No"])
    with col_filters[1]:
        selected_booking = st.selectbox("🪑 Table Booking", ["All", "Yes", "No"])
    with col_filters[2]:
        selected_rate = st.slider("⭐ Minimum Rating Score", 1.0, 5.0, 3.0, 0.1)

    # Fetch Data Securely
    try:
        df_filtered = db_utils.get_filtered_restaurants(
            min_rating=selected_rate,
            location=selected_location,
            online_order=selected_online,
            book_table=selected_booking,
            search_name=search_name,
        )
    except Exception as e:
        st.error(f"⚠️ Failed to query restaurants: {e}")
        st.stop()

    # Display Metrics Summary
    st.markdown("### 📊 Metrics Overview")
    vu.render_metric_cards(df_filtered, context="restaurants")

    st.markdown("---")

    # Display Results & Toggle
    tab1, tab2, tab3 = st.tabs(["📋 Filtered Results", "🛡️ Security Check", "ℹ️ Guide"])

    with tab1:
        st.markdown(f"**Found {len(df_filtered)} matching establishments:**")
        if not df_filtered.empty:
            st.dataframe(df_filtered, use_container_width=True)
        else:
            st.info("No restaurants match the selected criteria. Try adjusting the filters.")

    with tab2:
        st.subheader("How your query was executed safely:")
        st.markdown(
            """
            To avoid SQL Injection, user inputs are never concatenated directly. The SQL engine executes the following structure:
            """
        )
        safe_sql_template = """
        SELECT DISTINCT name, location, cuisines, rate, votes, online_order, book_table, approx_cost_fortwo, restaurant_type
        FROM restaurants
        WHERE rate >= ?
        """
        if selected_location != "All":
            safe_sql_template += "\n  AND location = ?"
        if selected_online != "All":
            safe_sql_template += "\n  AND online_order = ?"
        if selected_booking != "All":
            safe_sql_template += "\n  AND book_table = ?"
        if search_name.strip():
            safe_sql_template += "\n  AND name LIKE ?"

        st.code(safe_sql_template, language="sql")
        
        st.markdown("**Parameters injected safely:**")
        params_show = [selected_rate]
        if selected_location != "All":
            params_show.append(selected_location)
        if selected_online != "All":
            params_show.append(selected_online)
        if selected_booking != "All":
            params_show.append(selected_booking)
        if search_name.strip():
            params_show.append(f"%{search_name}%")
            
        st.write(params_show)

    with tab3:
        st.markdown(
            """
            ### 💡 Data Science Advice for Restaurateurs:
            - **High Rating Density**: Target locations with high ratings but lower restaurant counts to tap into underserved quality demand.
            - **Table Bookings**: High-rating restaurants frequently offer table booking. It correlates with larger basket sizes and higher customer satisfaction.
            """
        )

# ============================================
# PAGE 2 - Q&A HUB
# ============================================
elif page == "❓ Business Q&A Hub":
    st.markdown(
        """
        <div class="header-banner">
            <h1>❓ Business Intelligence Q&A Hub</h1>
            <p>Answer complex business questions regarding market entry, cost distributions, and cuisines.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    questions_map = {
        "Q1 - Top Rated Locations": (
            "Which locations in Bangalore have the highest average restaurant ratings?",
            """
            SELECT location, ROUND(AVG(rate),2) as avg_rating,
            COUNT(name) as total_restaurants
            FROM restaurants
            GROUP BY location
            ORDER BY avg_rating DESC LIMIT 10
            """,
            "bar_loc_rating",
            "This query identifies top-rated hubs. Useful for premium brand placement."
        ),
        "Q2 - Over Saturated Locations": (
            "Which locations have the highest density/number of restaurants?",
            """
            SELECT location, COUNT(name) as total_restaurants
            FROM restaurants
            GROUP BY location
            ORDER BY total_restaurants DESC LIMIT 10
            """,
            "bar_loc_count",
            "Identifies red-ocean markets. High count implies stiff competition."
        ),
        "Q3 - Online Ordering Impact": (
            "Does enabling online ordering relate to higher ratings?",
            """
            SELECT online_order, ROUND(AVG(rate),2) as avg_rating,
            COUNT(name) as total_restaurants
            FROM restaurants GROUP BY online_order
            """,
            "impact_online",
            "Compares online ordering presence against user satisfaction."
        ),
        "Q4 - Table Booking Impact": (
            "Does offering table booking correlate with better user ratings?",
            """
            SELECT book_table, ROUND(AVG(rate),2) as avg_rating,
            COUNT(name) as total_restaurants
            FROM restaurants GROUP BY book_table
            """,
            "impact_booking",
            "Assess value-add services. Table booking often indicates premium sit-down venues."
        ),
        "Q5 - Best Price Range": (
            "Which cost bracket yields the highest average rating?",
            """
            SELECT CASE 
                WHEN approx_cost_fortwo < 500 THEN 'Low'
                WHEN approx_cost_fortwo BETWEEN 500 AND 800 THEN 'Mid'
                ELSE 'Premium' END as price_segment,
            ROUND(AVG(rate),2) as avg_rating
            FROM restaurants
            GROUP BY price_segment
            ORDER BY avg_rating DESC LIMIT 1
            """,
            "metric_segment",
            "Identifies the target market sweet spot based on user review averages."
        ),
        "Q6 - Price Segment Performance": (
            "How are restaurants distributed across price tiers, and what are their ratings?",
            """
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
            "bar_price_segment",
            "Gives a broader breakdown of pricing strategy distribution vs ratings."
        ),
        "Q7 - Most Common Cuisines": (
            "What are the top 10 most common cuisines served in Bangalore?",
            """
            SELECT cuisines, COUNT(name) as total_restaurants
            FROM restaurants
            GROUP BY cuisines
            ORDER BY total_restaurants DESC LIMIT 10
            """,
            "bar_cuisines_common",
            "Identifies mainstream cuisine patterns. Good for mass market entries."
        ),
        "Q8 - Highest Rated Cuisines": (
            "What are the top 10 highest-rated cuisines?",
            """
            SELECT cuisines, ROUND(AVG(rate),2) as avg_rating
            FROM restaurants
            GROUP BY cuisines
            ORDER BY avg_rating DESC LIMIT 10
            """,
            "bar_cuisines_rated",
            "Shows which cuisines are receiving the highest ratings from consumers."
        ),
        "Q9 - Niche Cuisine Opportunities": (
            "Which cuisines are high-rated (>4.0) but low in competition (<10 restaurants)?",
            """
            SELECT cuisines, ROUND(AVG(rate),2) as avg_rating,
            COUNT(name) as total_restaurants
            FROM restaurants
            GROUP BY cuisines
            HAVING AVG(rate) > 4.0 AND COUNT(name) < 10
            ORDER BY avg_rating DESC LIMIT 10
            """,
            "bar_niche",
            "Discovers blue-ocean niche opportunities where quality is high but choice is rare."
        ),
        "Q10 - Cost vs Rating": (
            "What is the average cost and rating across the different budget tiers?",
            """
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
            "scatter_cost_rating",
            "Evaluates price elasticity and rating distributions together."
        )
    }

    selected_q = st.selectbox("📌 Select Business Question", list(questions_map.keys()))
    desc, sql, chart_type, biz_help = questions_map[selected_q]

    st.markdown(f"**Description**: {desc}")
    st.info(f"💡 **Business Purpose**: {biz_help}")

    # Session State management to prevent resetting filters/checkboxes on action reruns
    if "qa_result" not in st.session_state:
        st.session_state.qa_result = None
    if "qa_selected" not in st.session_state:
        st.session_state.qa_selected = None

    # Reset results if question changes
    if st.session_state.qa_selected != selected_q:
        st.session_state.qa_result = None
        st.session_state.qa_selected = selected_q

    if st.button("🔍 Run Analysis", type="primary"):
        try:
            st.session_state.qa_result = db_utils.run_query(sql)
        except Exception as e:
            st.error(f"⚠️ Failed to execute query: {e}")
            st.session_state.qa_result = None

    if st.session_state.qa_result is not None:
        df_result = st.session_state.qa_result

        st.markdown("---")
        st.markdown("### 📊 Interactive Control Panel")
        
        # Interactive themed option cards using images
        col_t1, col_t2, col_t3 = st.columns(3)
        with col_t1:
            if os.path.exists("assets/menu_receipt_data.png"):
                st.image("assets/menu_receipt_data.png", width=100)
            show_raw = st.checkbox("📋 Show Menu Sheet (Raw Data)", value=False)
        with col_t2:
            if os.path.exists("assets/sql_recipe_book.png"):
                st.image("assets/sql_recipe_book.png", width=100)
            show_sql = st.checkbox("💻 Show Cooking Recipe (SQL Code)", value=False)
        with col_t3:
            if os.path.exists("assets/chef_intelligence_brain.png"):
                st.image("assets/chef_intelligence_brain.png", width=100)
            show_theory = st.checkbox("🧠 Show Chef Intelligence (DS Theory)", value=True)

        st.markdown("---")
        
        # Plot matching chart
        st.markdown("### 📈 Visual Presentation")
        if chart_type == "bar_loc_rating":
            vu.plot_top_rated_locations(df_result)
        elif chart_type == "bar_loc_count":
            vu.plot_over_saturated_locations(df_result)
        elif chart_type == "impact_online":
            vu.plot_binary_impact(df_result, "online_order", "Online Ordering Impact on Ratings")
        elif chart_type == "impact_booking":
            vu.plot_binary_impact(df_result, "book_table", "Table Booking Impact on Ratings")
        elif chart_type == "metric_segment":
            if not df_result.empty:
                seg = df_result.iloc[0]['price_segment']
                rat = df_result.iloc[0]['avg_rating']
                st.metric("Best Performing Price Segment", f"{seg} Cost Tier", f"{rat} ⭐ avg rating")
        elif chart_type == "bar_price_segment":
            vu.plot_price_segment_performance(df_result)
        elif chart_type == "bar_cuisines_common":
            vu.plot_common_cuisines(df_result)
        elif chart_type == "bar_cuisines_rated":
            vu.plot_highest_rated_cuisines(df_result, "Top 10 Highest Rated Cuisines")
        elif chart_type == "bar_niche":
            vu.plot_highest_rated_cuisines(df_result, "Top 10 High Rating Niche Cuisine Opportunities")
        elif chart_type == "scatter_cost_rating":
            vu.plot_cost_vs_rating(df_result)

        # Handle Toggles
        if show_raw:
            st.markdown("### 📋 Menu Sheet (Raw Query Result)")
            st.dataframe(df_result, use_container_width=True)

        if show_sql:
            st.markdown("### 💻 SQL Cooking Recipe")
            st.code(sql, language="sql")

        if show_theory:
            # Data Science theory section
            st.markdown("### 🧠 Chef Intelligence (Data Science Theory)")
            if "Impact" in selected_q:
                st.markdown(
                    """
                    **Theory Check - Correlation vs. Causation:**
                    Providing value-added features like table bookings or online ordering correlates with higher average ratings. 
                    However, this doesn't automatically cause higher satisfaction. Restaurants offering table booking are often premium 
                    establishments with professional chefs, which naturally boost customer satisfaction.
                    """
                )
            elif "Niche" in selected_q:
                st.markdown(
                    """
                    **Theory Check - Market Opportunities:**
                    In competitive markets, serving mainstream cuisines (e.g. North Indian or Chinese) puts you in direct competition 
                    with thousands of outlets. Identifying high-rating cuisines with fewer competitors (niche) helps capture high-margin 
                    customer subsets.
                    """
                )
            else:
                st.markdown(
                    """
                    **Theory Check - Segment Aggregations:**
                    Using SQL groups (`GROUP BY`) allows us to bucket records to find statistical averages. This reveals overall system performance 
                    rather than individual outlier behaviors.
                    """
                )

# ============================================
# PAGE 3 - ORDERS INTELLIGENCE
# ============================================
elif page == "📦 Orders Intelligence":
    st.markdown(
        """
        <div class="header-banner">
            <h1>📦 Orders Intelligence</h1>
            <p>Deep-dive into payment methods, platform revenue trends, and discount behavior.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    order_questions = {
        "OQ1 - Payment Method Revenue": (
            "What is the revenue generated by different payment methods?",
            """
            SELECT payment_method, COUNT(*) as total_orders,
            ROUND(SUM(order_value),2) as total_revenue
            FROM orders GROUP BY payment_method
            ORDER BY total_revenue DESC
            """,
            "pie_payment",
            "Identifies preference patterns for payment gateways to negotiate fee splits."
        ),
        "OQ2 - Discount Impact": (
            "Do discounts increase the average order size (basket size)?",
            """
            SELECT discount_used, COUNT(*) as total_orders,
            ROUND(AVG(order_value),2) as avg_order_value
            FROM orders GROUP BY discount_used
            """,
            "bar_discount",
            "Evaluates promotion elasticity: do discounts encourage higher spending per order?"
        ),
        "OQ3 - Revenue by Day": (
            "Which days of the week generate the most revenue?",
            """
            SELECT 
                CASE strftime('%w', order_date)
                    WHEN '0' THEN 'Sunday'
                    WHEN '1' THEN 'Monday'
                    WHEN '2' THEN 'Tuesday'
                    WHEN '3' THEN 'Wednesday'
                    WHEN '4' THEN 'Thursday'
                    WHEN '5' THEN 'Friday'
                    WHEN '6' THEN 'Saturday'
                END as day_of_week,
                COUNT(*) as total_orders,
                ROUND(SUM(order_value),2) as total_revenue,
                ROUND(AVG(order_value),2) as avg_order_value
            FROM orders
            GROUP BY day_of_week
            ORDER BY total_revenue DESC
            """,
            "line_day",
            "Helps staff kitchens and schedule delivery partners based on demand cycles."
        ),
        "OQ4 - Top Restaurants by Revenue": (
            "Who are the top 10 restaurants contributing to platform sales?",
            """
            SELECT restaurant_name, COUNT(*) as total_orders,
            ROUND(SUM(order_value),2) as total_revenue
            FROM orders GROUP BY restaurant_name
            ORDER BY total_revenue DESC LIMIT 10
            """,
            "bar_restaurants",
            "Finds key account restaurants that are critical for commissions."
        ),
        "OQ5 - Monthly Revenue": (
            "What is the monthly sales trend on the platform?",
            """
            SELECT 
                CASE strftime('%m', order_date)
                    WHEN '01' THEN 'January'
                    WHEN '02' THEN 'February'
                    WHEN '03' THEN 'March'
                    WHEN '04' THEN 'April'
                    WHEN '05' THEN 'May'
                    WHEN '06' THEN 'June'
                    WHEN '07' THEN 'July'
                    WHEN '08' THEN 'August'
                    WHEN '09' THEN 'September'
                    WHEN '10' THEN 'October'
                    WHEN '11' THEN 'November'
                    WHEN '12' THEN 'December'
                END as month,
                COUNT(*) as total_orders,
                ROUND(SUM(order_value),2) as total_revenue
            FROM orders
            GROUP BY month
            ORDER BY total_revenue DESC
            """,
            "bar_month",
            "Visualizes seasonality of order volumes across months."
        ),
        "OQ6 - Payment + Discount Combined": (
            "How do discounts interact with payment methods in driving sales?",
            """
            SELECT payment_method, discount_used,
            COUNT(*) as total_orders,
            ROUND(SUM(order_value),2) as total_revenue
            FROM orders GROUP BY payment_method, discount_used
            ORDER BY total_revenue DESC
            """,
            "bar_combined",
            "Informs joint promo plans (e.g. Card discount partnerships)."
        )
    }

    selected_oq = st.selectbox("📌 Select Order Analysis", list(order_questions.keys()))
    desc, sql, chart_type, biz_help = order_questions[selected_oq]

    st.markdown(f"**Description**: {desc}")
    st.info(f"💡 **Business Purpose**: {biz_help}")

    # Session State management to prevent resetting filters/checkboxes on action reruns
    if "order_result" not in st.session_state:
        st.session_state.order_result = None
    if "order_selected" not in st.session_state:
        st.session_state.order_selected = None

    # Reset results if question changes
    if st.session_state.order_selected != selected_oq:
        st.session_state.order_result = None
        st.session_state.order_selected = selected_oq

    if st.button("🔍 Run Analysis", type="primary"):
        try:
            st.session_state.order_result = db_utils.run_query(sql)
        except Exception as e:
            st.error(f"⚠️ Failed to execute query: {e}")
            st.session_state.order_result = None

    if st.session_state.order_result is not None:
        df_result = st.session_state.order_result

        st.markdown("---")
        st.markdown("### 📊 Interactive Control Panel")
        
        # Interactive themed option cards using images
        col_t1, col_t2, col_t3 = st.columns(3)
        with col_t1:
            if os.path.exists("assets/menu_receipt_data.png"):
                st.image("assets/menu_receipt_data.png", width=100)
            show_raw = st.checkbox("📋 Show Order Receipts (Raw Data)", value=False)
        with col_t2:
            if os.path.exists("assets/sql_recipe_book.png"):
                st.image("assets/sql_recipe_book.png", width=100)
            show_sql = st.checkbox("💻 Show Cooking Recipe (SQL Code)", value=False)
        with col_t3:
            if os.path.exists("assets/chef_intelligence_brain.png"):
                st.image("assets/chef_intelligence_brain.png", width=100)
            show_theory = st.checkbox("🧠 Show Chef Intelligence (DS Theory)", value=True)

        st.markdown("---")

        # Plot charts
        st.markdown("### 📈 Visual Presentation")
        if chart_type == "pie_payment":
            vu.plot_payment_revenue(df_result)
        elif chart_type == "bar_discount":
            vu.plot_discount_impact(df_result)
        elif chart_type == "line_day":
            vu.plot_revenue_by_day(df_result)
        elif chart_type == "bar_restaurants":
            vu.plot_top_restaurants_revenue(df_result)
        elif chart_type == "bar_month":
            vu.plot_monthly_revenue(df_result)
        elif chart_type == "bar_combined":
            vu.plot_payment_discount_combined(df_result)

        # Handle Toggles
        if show_raw:
            st.markdown("### 📋 Order Receipts (Raw Query Result)")
            st.dataframe(df_result, use_container_width=True)

        if show_sql:
            st.markdown("### 💻 SQL Cooking Recipe")
            st.code(sql, language="sql")

        if show_theory:
            # Data Science theory section
            st.markdown("### 🧠 Chef Intelligence (Data Science Theory)")
            if "Discount" in selected_oq:
                st.markdown(
                    """
                    **Theory Check - Incentives & Elasticity:**
                    Discounts reduce immediate unit margins but increase the average basket size. If customers spend more per order when 
                    using a discount, the volume effect might offset the lower margins.
                    """
                )
            elif "Day" in selected_oq or "Month" in selected_oq:
                st.markdown(
                    """
                    **Theory Check - Seasonality and Trends:**
                    Time-series parsing (like `strftime` in SQLite) helps extract temporal patterns. E.g., showing weekend spikes or 
                    mid-week slumps, which is critical for planning campaigns.
                    """
                )
            else:
                st.markdown(
                    """
                    **Theory Check - Joint Distributions:**
                    Groupings by multiple features (e.g., payment type and discount utilization) reveal conditional interactions. 
                    For instance, users paying by credit cards with discounts applied may represent the highest-margin transactions.
                    """
                )