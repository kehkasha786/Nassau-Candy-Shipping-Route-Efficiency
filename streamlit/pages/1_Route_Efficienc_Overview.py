import streamlit as st
import pandas as pd
import plotly.express as px
from Styles import apply_custom_style, render_sidebar

st.set_page_config(page_title="Route Efficiency", page_icon="🍬", layout="wide")
apply_custom_style()
render_sidebar()

route_efficiency = pd.read_csv("data/route_efficiency.csv")
top_routes = pd.read_csv("data/top_10_routes.csv")
bottom_routes = pd.read_csv("data/bottom_10_routes.csv")
high_volume_poor_performance = pd.read_csv("data/high_volume_poor_performance.csv")

st.title("Route Efficiency")
st.markdown(
    "Routes are ranked using a normalized Efficiency Score (0-100, higher is better). "
    "Scores are relative comparisons across routes, not literal shipping durations."
)

st.divider()

st.subheader("Route Leaderboard")

st.dataframe(
    route_efficiency.sort_values("Efficiency_Score", ascending=False),
    use_container_width=True,
    hide_index=True
)

st.divider()

st.subheader("Top 10 Most Efficient Routes")

fig_top = px.bar(
    top_routes.sort_values("Efficiency_Score", ascending=True),
    x="Efficiency_Score",
    y="Route_State",
    orientation="h"
)
fig_top.update_layout(bargap=0.3)
st.plotly_chart(fig_top, use_container_width=True)

st.divider()

st.subheader("Bottom 10 Least Efficient Routes")

fig_bottom = px.bar(
    bottom_routes.sort_values("Efficiency_Score", ascending=False),
    x="Efficiency_Score",
    y="Route_State",
    orientation="h"
)
fig_bottom.update_layout(bargap=0.3)
st.plotly_chart(fig_bottom, use_container_width=True)

st.divider()

st.subheader("High-Volume, Poor-Performance Routes")
st.markdown(
    "Routes with above-average shipment volume **and** above-average Lead Time — "
    "these matter most operationally, since they combine real business impact with "
    "underperformance, unlike low-volume statistical outliers."
)

st.dataframe(
    high_volume_poor_performance,
    use_container_width=True,
    hide_index=True
)
