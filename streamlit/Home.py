import streamlit as st
import pandas as pd
import plotly.express as px
from Styles import apply_custom_style, render_sidebar, kpi_card

# -----------------------------
# Page Configuration
# -----------------------------
st.set_page_config(
    page_title="Nassau Candy - Shipping Route Analysis",
    page_icon="🍬",
    layout="wide"
)

apply_custom_style()
render_sidebar()

# -----------------------------
# Load Data
# -----------------------------
df = pd.read_csv("data/nassau_candy_cleaned.csv")
route_efficiency = pd.read_csv("data/route_efficiency.csv")
route_delay = pd.read_csv("data/route_delay_frequency.csv")
ship_mode_stats = pd.read_csv("data/ship_mode_performance.csv")

# -----------------------------
# Title
# -----------------------------
st.title("🍬 Nassau Candy Distributor")
st.subheader("Factory-to-Customer Shipping Route Efficiency Analysis")

st.markdown(
    "Analyze shipping performance, route efficiency, geographic bottlenecks, "
    "and shipping mode performance."
)

# -----------------------------
# Overview Content
# -----------------------------
st.header("Overview")

st.write(
    "This dashboard provides an executive overview of Nassau Candy's "
    "factory-to-customer shipping performance."
)

# -----------------------------
# Headline KPI Cards
# -----------------------------
total_orders = df["Order ID"].nunique()
total_sales = df["Sales"].sum()
total_gross_profit = df["Gross Profit"].sum()

delay_threshold = 1634

total_orders_check = df["Order ID"].nunique()
delayed_orders = df.loc[df["Lead Time"] >= delay_threshold, "Order ID"].nunique()
overall_delay_freq = delayed_orders / total_orders_check * 100
avg_efficiency_score = route_efficiency["Efficiency_Score"].mean()

col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    kpi_card("Total Orders", f"{total_orders:,}", accent="#F5A623")
with col2:
    kpi_card("Total Sales", f"${total_sales:,.0f}", accent="#F5A623")
with col3:
    kpi_card("Total Gross Profit", f"${total_gross_profit:,.0f}", accent="#3DDC97")
with col4:
    kpi_card("Overall Delay Frequency", f"{overall_delay_freq:.2f}%", accent="#E63950")
with col5:
    kpi_card("Avg Efficiency Score", f"{avg_efficiency_score:.1f}/100", accent="#3DDC97")

# -----------------------------
# Overview Charts
# -----------------------------
st.divider()

st.subheader("Orders by Ship Mode")
ship_mode_orders = (
    df.groupby("Ship Mode")["Order ID"]
    .nunique()
    .sort_values(ascending=False)
    .reset_index(name="Orders")
)
fig1 = px.bar(ship_mode_orders, x="Ship Mode", y="Orders")
fig1.update_layout(bargap=0.7)
st.plotly_chart(fig1, use_container_width="stretch")

st.subheader("Orders by Factory")
factory_orders = (
    df.groupby("Factory")["Order ID"]
    .nunique()
    .sort_values(ascending=False)
    .reset_index(name="Orders")
)
fig2 = px.bar(factory_orders, x="Factory", y="Orders")
fig2.update_layout(bargap=0.7)
st.plotly_chart(fig2, use_container_width="stretch")


