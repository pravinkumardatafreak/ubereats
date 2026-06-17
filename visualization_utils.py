"""Visualization utility module for Uber Eats Bangalore Restaurant Intelligence.

This module provides interactive plotting functions using Plotly Express,
styled to match professional design guidelines (using Uber Eats brand colors
and clean typography). It conforms to PEP-8 coding standards.
"""

import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

# Standard Brand Colors (Uber Eats green and elegant supporting shades)
UBER_GREEN = "#06C167"
DARK_CHARCOAL = "#1F1F1F"
SLATE_GRAY = "#7F8C8D"
GOLDEN_YELLOW = "#F1C40F"
CORAL_ORANGE = "#E67E22"
SOFT_BLUE = "#3498DB"

PLOTLY_THEME = "plotly_white"


def render_metric_cards(df: pd.DataFrame, context: str = "restaurants"):
    """Render high-level metric cards in Streamlit layout.

    Args:
        df (pd.DataFrame): The data used to compute metrics.
        context (str): The dataset context ('restaurants' or 'orders').
    """
    cols = st.columns(3)

    if context == "restaurants":
        if df.empty:
            total_restaurants = 0
            avg_rate = 0.0
            avg_cost = 0.0
        else:
            total_restaurants = len(df)
            avg_rate = df["rate"].mean() if "rate" in df.columns else 0
            avg_cost = df["approx_cost_fortwo"].mean() if "approx_cost_fortwo" in df.columns else 0

        with cols[0]:
            st.metric(
                label="Total Restaurants",
                value=f"{total_restaurants:,}",
                help="Total unique restaurants matching current filters",
            )
        with cols[1]:
            st.metric(
                label="Average Rating",
                value=f"{avg_rate:.2f} ⭐" if avg_rate > 0 else "N/A",
                help="Mean rating score across the matching subset",
            )
        with cols[2]:
            st.metric(
                label="Avg Cost for Two",
                value=f"₹{avg_cost:.2f}" if avg_cost > 0 else "N/A",
                help="Mean cost for two people",
            )

    elif context == "orders":
        if df.empty:
            total_orders = 0
            total_revenue = 0.0
            avg_order = 0.0
        else:
            total_orders = len(df)
            total_revenue = df["order_value"].sum() if "order_value" in df.columns else 0
            avg_order = df["order_value"].mean() if "order_value" in df.columns else 0

        with cols[0]:
            st.metric(
                label="Total Volume",
                value=f"{total_orders:,} Orders",
                help="Total orders placed in the system",
            )
        with cols[1]:
            st.metric(
                label="Gross Revenue",
                value=f"₹{total_revenue:,.2f}",
                help="Cumulative order values before discounts",
            )
        with cols[2]:
            st.metric(
                label="Avg Basket Size (AOV)",
                value=f"₹{avg_order:.2f}",
                help="Average Order Value across transactions",
            )


def plot_top_rated_locations(df: pd.DataFrame):
    """Plot Q1 - Top Rated Locations horizontal bar chart."""
    df_sorted = df.sort_values(by="avg_rating", ascending=True)
    fig = px.bar(
        df_sorted,
        x="avg_rating",
        y="location",
        orientation="h",
        title="Top 10 Locations by Average Rating",
        labels={"avg_rating": "Average Rating (out of 5)", "location": "Location"},
        color="avg_rating",
        color_continuous_scale=[[0, "#A3E4D7"], [1, UBER_GREEN]],
        text_auto=".2f",
    )
    fig.update_layout(template=PLOTLY_THEME, coloraxis_showscale=False, height=450)
    fig.update_traces(textposition="outside", cliponaxis=False)
    st.plotly_chart(fig, use_container_width=True)


def plot_over_saturated_locations(df: pd.DataFrame):
    """Plot Q2 - Over Saturated Locations vertical bar chart."""
    fig = px.bar(
        df,
        x="location",
        y="total_restaurants",
        title="Top 10 Most Saturated Locations (Restaurant Count)",
        labels={"total_restaurants": "Number of Restaurants", "location": "Location"},
        color_discrete_sequence=[CORAL_ORANGE],
        text_auto=True,
    )
    fig.update_layout(template=PLOTLY_THEME, height=450)
    fig.update_traces(textposition="outside")
    st.plotly_chart(fig, use_container_width=True)


def plot_binary_impact(df: pd.DataFrame, x_col: str, title: str):
    """Plot Q3/Q4 - Impact of Online Order or Table Booking on Ratings."""
    fig = px.bar(
        df,
        x=x_col,
        y="avg_rating",
        title=title,
        labels={"avg_rating": "Average Rating", x_col: x_col.replace("_", " ").title()},
        color=x_col,
        color_discrete_map={"Yes": UBER_GREEN, "No": SLATE_GRAY},
        text_auto=".2f",
    )
    fig.update_layout(template=PLOTLY_THEME, showlegend=False, height=400)
    fig.update_traces(textposition="outside")
    st.plotly_chart(fig, use_container_width=True)


def plot_price_segment_performance(df: pd.DataFrame):
    """Plot Q6 - Price Segment Performance grouped chart."""
    fig = px.bar(
        df,
        x="price_segment",
        y="total_restaurants",
        color="avg_rating",
        title="Price Segment: Distribution & Average Rating Performance",
        labels={
            "total_restaurants": "Restaurant Count",
            "price_segment": "Cost Tier",
            "avg_rating": "Avg Rating",
        },
        color_continuous_scale="Viridis",
        text_auto=True,
    )
    fig.update_layout(template=PLOTLY_THEME, height=450)
    st.plotly_chart(fig, use_container_width=True)


def plot_common_cuisines(df: pd.DataFrame):
    """Plot Q7 - Most Common Cuisines horizontal bar chart."""
    df_sorted = df.sort_values(by="total_restaurants", ascending=True)
    fig = px.bar(
        df_sorted,
        x="total_restaurants",
        y="cuisines",
        orientation="h",
        title="Top 10 Most Common Cuisines in Bangalore",
        labels={"total_restaurants": "Number of Restaurants", "cuisines": "Cuisine Group"},
        color_discrete_sequence=[SOFT_BLUE],
        text_auto=True,
    )
    fig.update_layout(template=PLOTLY_THEME, height=450)
    fig.update_traces(textposition="outside", cliponaxis=False)
    st.plotly_chart(fig, use_container_width=True)


def plot_highest_rated_cuisines(df: pd.DataFrame, title: str):
    """Plot Q8/Q9 - Highest Rated or Niche Cuisines horizontal bar chart."""
    df_sorted = df.sort_values(by="avg_rating", ascending=True)
    fig = px.bar(
        df_sorted,
        x="avg_rating",
        y="cuisines",
        orientation="h",
        title=title,
        labels={"avg_rating": "Average Rating", "cuisines": "Cuisine"},
        color="avg_rating",
        color_continuous_scale="Cividis",
        text_auto=".2f",
    )
    fig.update_layout(template=PLOTLY_THEME, coloraxis_showscale=False, height=450)
    fig.update_traces(textposition="outside", cliponaxis=False)
    st.plotly_chart(fig, use_container_width=True)


def plot_cost_vs_rating(df: pd.DataFrame):
    """Plot Q10 - Cost vs Rating Scatter Plot."""
    fig = px.scatter(
        df,
        x="avg_cost",
        y="avg_rating",
        color="cost_category",
        size="avg_cost",
        title="Cost vs Rating Trend Analysis",
        labels={
            "avg_cost": "Average Cost for Two (₹)",
            "avg_rating": "Average Rating Score",
            "cost_category": "Cost Category",
        },
        hover_data=["cost_category", "avg_cost", "avg_rating"],
    )
    fig.update_layout(template=PLOTLY_THEME, height=450)
    st.plotly_chart(fig, use_container_width=True)


def plot_payment_revenue(df: pd.DataFrame):
    """Plot OQ1 - Payment Method Revenue donut chart."""
    fig = px.pie(
        df,
        values="total_revenue",
        names="payment_method",
        title="Revenue Contribution by Payment Method",
        hole=0.4,
        color_discrete_sequence=[UBER_GREEN, SOFT_BLUE, CORAL_ORANGE, GOLDEN_YELLOW],
    )
    fig.update_layout(template=PLOTLY_THEME, height=400)
    st.plotly_chart(fig, use_container_width=True)


def plot_discount_impact(df: pd.DataFrame):
    """Plot OQ2 - Discount Impact bar chart."""
    fig = px.bar(
        df,
        x="discount_used",
        y="avg_order_value",
        title="Discount Impact on Average Order Value (AOV)",
        labels={
            "avg_order_value": "Average Order Value (₹)",
            "discount_used": "Discount Applied?",
        },
        color="discount_used",
        color_discrete_map={"Yes": UBER_GREEN, "No": SLATE_GRAY},
        text_auto=".2f",
    )
    fig.update_layout(template=PLOTLY_THEME, showlegend=False, height=400)
    fig.update_traces(textposition="outside")
    st.plotly_chart(fig, use_container_width=True)


def plot_revenue_by_day(df: pd.DataFrame):
    """Plot OQ3 - Revenue by Day of Week sorted logically."""
    # Ensure standard weekly order
    day_order = [
        "Monday",
        "Tuesday",
        "Wednesday",
        "Thursday",
        "Friday",
        "Saturday",
        "Sunday",
    ]
    df["day_of_week"] = pd.Categorical(df["day_of_week"], categories=day_order, ordered=True)
    df_sorted = df.sort_values("day_of_week")

    fig = px.line(
        df_sorted,
        x="day_of_week",
        y="total_revenue",
        title="Revenue Trend Across Days of the Week",
        labels={"total_revenue": "Total Revenue (₹)", "day_of_week": "Day of Week"},
        markers=True,
    )
    fig.update_traces(line_color=UBER_GREEN, line_width=3, marker_size=8)
    fig.update_layout(template=PLOTLY_THEME, height=400)
    st.plotly_chart(fig, use_container_width=True)


def plot_top_restaurants_revenue(df: pd.DataFrame):
    """Plot OQ4 - Top Restaurants by Revenue horizontal bar chart."""
    df_sorted = df.sort_values(by="total_revenue", ascending=True)
    fig = px.bar(
        df_sorted,
        x="total_revenue",
        y="restaurant_name",
        orientation="h",
        title="Top 10 Restaurants by Platform Revenue",
        labels={"total_revenue": "Total Sales (₹)", "restaurant_name": "Restaurant"},
        color_discrete_sequence=[UBER_GREEN],
        text_auto=",.0f",
    )
    fig.update_layout(template=PLOTLY_THEME, height=450)
    fig.update_traces(textposition="outside", cliponaxis=False)
    st.plotly_chart(fig, use_container_width=True)


def plot_monthly_revenue(df: pd.DataFrame):
    """Plot OQ5 - Monthly Revenue Trend."""
    month_order = [
        "January",
        "February",
        "March",
        "April",
        "May",
        "June",
        "July",
        "August",
        "September",
        "October",
        "November",
        "December",
    ]
    df["month"] = pd.Categorical(df["month"], categories=month_order, ordered=True)
    df_sorted = df.sort_values("month")

    fig = px.bar(
        df_sorted,
        x="month",
        y="total_revenue",
        title="Monthly Revenue Analytics",
        labels={"total_revenue": "Monthly Revenue (₹)", "month": "Month"},
        color_discrete_sequence=[SOFT_BLUE],
        text_auto=",.0f",
    )
    fig.update_layout(template=PLOTLY_THEME, height=400)
    fig.update_traces(textposition="outside")
    st.plotly_chart(fig, use_container_width=True)


def plot_payment_discount_combined(df: pd.DataFrame):
    """Plot OQ6 - Payment and Discount interactions."""
    fig = px.bar(
        df,
        x="payment_method",
        y="total_revenue",
        color="discount_used",
        title="Revenue Breakup by Payment & Discount Combination",
        labels={
            "total_revenue": "Total Revenue (₹)",
            "payment_method": "Payment Method",
            "discount_used": "Discount Used?",
        },
        barmode="group",
        color_discrete_map={"Yes": UBER_GREEN, "No": SLATE_GRAY},
    )
    fig.update_layout(template=PLOTLY_THEME, height=450)
    st.plotly_chart(fig, use_container_width=True)
