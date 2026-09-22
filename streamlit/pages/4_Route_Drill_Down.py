import streamlit as st
import pandas as pd
from Styles import apply_custom_style, render_sidebar

st.set_page_config(page_title="Route Drill-Down", page_icon="🍬", layout="wide")
apply_custom_style()
render_sidebar()

df = pd.read_csv("data/nassau_candy_cleaned.csv")

st.title("Route Drill-Down")
st.markdown("Select a state below to explore order and product-line shipment details for that destination.")

selected_state = st.selectbox(
    "Select a State",
    sorted(df["State/Province"].unique())
)

filtered_df = df[df["State/Province"] == selected_state]

st.divider()

ship_mode_options = ["All"] + sorted(df["Ship Mode"].unique().tolist())
selected_ship_mode = st.selectbox("Filter by Ship Mode (optional)", ship_mode_options)

if selected_ship_mode != "All":
    filtered_df = filtered_df[filtered_df["Ship Mode"] == selected_ship_mode]

st.divider()
st.subheader("Additional Filters")

col_a, col_b = st.columns(2)

with col_a:
    min_date = df["Order Date"].min()
    max_date = df["Order Date"].max()
    date_range = st.date_input(
        "Order Date Range",
        value=(pd.to_datetime(min_date), pd.to_datetime(max_date)),
        min_value=pd.to_datetime(min_date),
        max_value=pd.to_datetime(max_date)
    )

with col_b:
    st.caption("Lead Time Threshold (relative segmentation, not literal shipping days — see Data Validation)")
    lead_time_threshold = st.slider(
        "Minimum Lead Time:",
        min_value=int(df["Lead Time"].min()),
        max_value=int(df["Lead Time"].max()),
        value=int(df["Lead Time"].min())
    )

# Apply State, Ship Mode and Date filters first
base_filtered_df = df[df["State/Province"] == selected_state]

if selected_ship_mode != "All":
    base_filtered_df = base_filtered_df[
        base_filtered_df["Ship Mode"] == selected_ship_mode
    ]

if len(date_range) == 2:
    base_filtered_df = base_filtered_df[
        (pd.to_datetime(base_filtered_df["Order Date"]) >= pd.to_datetime(date_range[0])) &
        (pd.to_datetime(base_filtered_df["Order Date"]) <= pd.to_datetime(date_range[1]))
    ]

# Apply Lead Time slider separately for drill-down
filtered_df = base_filtered_df[
    base_filtered_df["Lead Time"] >= lead_time_threshold
]

st.write(
    f"Showing {filtered_df['Order ID'].nunique()} orders for **{selected_state}**"
    + (f" — **{selected_ship_mode}**" if selected_ship_mode != "All" else "")
    + f" with Lead Time ≥ {lead_time_threshold}"
)

st.divider()

col1, col2, col3 = st.columns(3)

col1.metric("Total Orders", f"{filtered_df['Order ID'].nunique():,}")
col2.metric("Total Sales", f"${filtered_df['Sales'].sum():,.2f}")

delay_threshold = 1634

base_orders = base_filtered_df["Order ID"].nunique()

delayed = base_filtered_df[
    base_filtered_df["Lead Time"] >= delay_threshold
]["Order ID"].nunique()

delay_pct = (
    round(delayed / base_orders * 100, 2)
    if base_orders > 0
    else 0
)
col3.metric("Delay Frequency", f"{delay_pct}%")

st.divider()
st.subheader("Factories Serving This State")
factory_breakdown = (
    filtered_df.groupby("Factory")["Order ID"]
    .nunique()
    .reset_index(name="Orders")
    .sort_values("Orders", ascending=False)
)
st.dataframe(factory_breakdown, width="stretch", hide_index=True)

st.divider()
st.subheader("Order-Level Shipment Details")
st.caption(
    "Ship Date is shown for reference only because the dataset contains a known "
    "date-generation anomaly. It should not be interpreted as literal shipment chronology."
)

timeline_df = filtered_df[["Order ID", "Order Date", "Ship Date", "Ship Mode", "Product Name", "Factory"]].sort_values("Order Date")

st.dataframe(timeline_df, width="stretch", hide_index=True)
