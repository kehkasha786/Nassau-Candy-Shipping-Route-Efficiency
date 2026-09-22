import streamlit as st
import pandas as pd
import plotly.express as px
from Styles import apply_custom_style, render_sidebar

st.set_page_config(page_title="Ship Mode Comparison", page_icon="🍬", layout="wide")
apply_custom_style()
render_sidebar()

df = pd.read_csv("data/nassau_candy_cleaned.csv")
ship_mode_stats = pd.read_csv("data/ship_mode_performance.csv")

st.title("Ship Mode Comparison")
st.markdown(
    "Comparing cost and shipping performance across Ship Mode categories. "
    "Lead Time values shown here are used for relative comparison between modes only."
)

st.divider()
st.subheader("Ship Mode Summary")
st.dataframe(ship_mode_stats, width="stretch", hide_index=True)

st.divider()
st.subheader("Average Lead Time by Ship Mode")

fig_leadtime = px.bar(
    ship_mode_stats.sort_values("Avg_Lead_Time"),
    x="Ship Mode",
    y="Avg_Lead_Time"
)
fig_leadtime.update_layout(bargap=0.6)
st.plotly_chart(fig_leadtime, width="stretch")

st.info(
     "**Data-quality note:** First Class and Same Day show higher average Lead Time "
    "than Standard Class in this dataset. Because the Order Date–Ship Date relationship "
    "contains a known date-generation anomaly, these Lead Time values should be interpreted "
    "as relative analytical measures rather than literal shipping durations."
)

st.divider()
st.subheader("Average Cost by Ship Mode")

fig_cost = px.bar(
    ship_mode_stats.sort_values("Avg_Cost_Per_Shipment", ascending=False),
    x="Ship Mode",
    y="Avg_Cost_Per_Shipment"
)
fig_cost.update_layout(bargap=0.6)
st.plotly_chart(fig_cost, width="stretch")

st.markdown(
    "Average cost per shipment is relatively similar across all four Ship Mode categories, "
    "ranging from approximately $4.42 to $4.84. Within this dataset, the cost differences "
    "do not correspond to a clear improvement in the relative Lead Time measure."
)
