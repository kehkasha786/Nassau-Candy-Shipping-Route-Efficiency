import streamlit as st
import pandas as pd
import plotly.express as px
from Styles import apply_custom_style, render_sidebar

st.set_page_config(page_title="Geographic Map", page_icon="🍬", layout="wide")
apply_custom_style()
render_sidebar()

df = pd.read_csv("data/nassau_candy_cleaned.csv")

st.title("Geographic Shipping Map")
st.markdown(
    "State-level shipping performance across the US. Efficiency Score is normalized (0-100); "
    "higher is better."
)
delay_threshold = 1634

state_summary = (
    df.groupby("State/Province")
    .agg(
        Order_Volume=("Order ID", "nunique"),
        Avg_Lead_Time=("Lead Time", "mean")
    )
    .reset_index()
)

# Delay Frequency per state (order-level, same logic as Phase 4A)
delayed_orders_by_state = (
    df[df["Lead Time"] >= delay_threshold]
    .groupby("State/Province")["Order ID"]
    .nunique()
    .reset_index(name="Delayed_Orders")
)

state_summary = state_summary.merge(delayed_orders_by_state, on="State/Province", how="left")
state_summary["Delayed_Orders"] = state_summary["Delayed_Orders"].fillna(0)
state_summary["Delay_Frequency_Pct"] = round(
    state_summary["Delayed_Orders"] / state_summary["Order_Volume"] * 100, 2
)

# Efficiency Score (0-100, same min-max logic as route-level)
min_lt = state_summary["Avg_Lead_Time"].min()
max_lt = state_summary["Avg_Lead_Time"].max()
state_summary["Efficiency_Score"] = round(
    100 * (max_lt - state_summary["Avg_Lead_Time"]) / (max_lt - min_lt), 2
)

state_summary

us_state_abbrev = {
    'Alabama': 'AL', 'Alaska': 'AK', 'Arizona': 'AZ', 'Arkansas': 'AR', 'California': 'CA',
    'Colorado': 'CO', 'Connecticut': 'CT', 'Delaware': 'DE', 'District of Columbia': 'DC',
    'Florida': 'FL', 'Georgia': 'GA', 'Hawaii': 'HI', 'Idaho': 'ID', 'Illinois': 'IL',
    'Indiana': 'IN', 'Iowa': 'IA', 'Kansas': 'KS', 'Kentucky': 'KY', 'Louisiana': 'LA',
    'Maine': 'ME', 'Maryland': 'MD', 'Massachusetts': 'MA', 'Michigan': 'MI', 'Minnesota': 'MN',
    'Mississippi': 'MS', 'Missouri': 'MO', 'Montana': 'MT', 'Nebraska': 'NE', 'Nevada': 'NV',
    'New Hampshire': 'NH', 'New Jersey': 'NJ', 'New Mexico': 'NM', 'New York': 'NY',
    'North Carolina': 'NC', 'North Dakota': 'ND', 'Ohio': 'OH', 'Oklahoma': 'OK', 'Oregon': 'OR',
    'Pennsylvania': 'PA', 'Rhode Island': 'RI', 'South Carolina': 'SC', 'South Dakota': 'SD',
    'Tennessee': 'TN', 'Texas': 'TX', 'Utah': 'UT', 'Vermont': 'VT', 'Virginia': 'VA',
    'Washington': 'WA', 'West Virginia': 'WV', 'Wisconsin': 'WI', 'Wyoming': 'WY'
}

state_summary["State_Code"] = state_summary["State/Province"].map(us_state_abbrev)

st.divider()
st.subheader("State-Level Efficiency Map")

fig_map = px.choropleth(
    state_summary,
    locations="State_Code",
    locationmode="USA-states",
    color="Efficiency_Score",
    scope="usa",
    color_continuous_scale="RdYlGn",
    hover_name="State/Province",
    hover_data={"State_Code": False, "Order_Volume": True, "Avg_Lead_Time": False, "Delay_Frequency_Pct": True}
)
st.plotly_chart(fig_map, width="stretch")

st.divider()
st.subheader("State-Level Delay Frequency Map")

fig_delay_map = px.choropleth(
    state_summary,
    locations="State_Code",
    locationmode="USA-states",
    color="Delay_Frequency_Pct",
    scope="usa",
    color_continuous_scale="Reds",
    hover_name="State/Province",
    hover_data={"State_Code": False, "Order_Volume": True, "Efficiency_Score": True}
)
st.plotly_chart(fig_delay_map, width="stretch")

st.divider()
st.subheader("Congestion-Prone States")
st.markdown(
    "States with above-average order volume **and** above-average Delay Frequency — "
    "these represent the most operationally significant bottlenecks."
)

avg_volume = state_summary["Order_Volume"].mean()
avg_delay = state_summary["Delay_Frequency_Pct"].mean()

congestion_prone = state_summary[
    (state_summary["Order_Volume"] > avg_volume) &
    (state_summary["Delay_Frequency_Pct"] > avg_delay)
].sort_values("Order_Volume", ascending=False)

st.dataframe(
    congestion_prone[["State/Province", "Order_Volume", "Delay_Frequency_Pct", "Efficiency_Score"]],
    width="stretch",
    hide_index=True
)
