import streamlit as st
import pandas as pd
import numpy as np

# ============================================================
# PAGE CONFIG
# ============================================================
st.set_page_config(
    page_title="Customer Analytics Dashboard",
    page_icon="📊",
    layout="wide",
)

ACTIVE_DAYS_THRESHOLD = 30  # days since last order to be considered "Active"


# ============================================================
# DATA LOADING (cached so the CSV isn't re-read on every filter change)
# ============================================================
@st.cache_data
def load_data(path: str) -> pd.DataFrame:
    df = pd.read_csv(path)
    df["order_date"] = pd.to_datetime(df["order_date"])
    df["total_price"] = df["price_after_discount"] * df["product_count"]
    return df


DATA_PATH = "sales_date.csv"

st.title("📊 Customer Analytics Dashboard")

try:
    raw_df = load_data(DATA_PATH)
except FileNotFoundError:
    st.error(
        f"Couldn't find `{DATA_PATH}`. Place it next to app.py, or update "
        "DATA_PATH / add a file uploader."
    )
    st.stop()

# Optional: let the user upload a different file instead of hardcoding the path
with st.sidebar:
    st.header("Data")
    uploaded = st.file_uploader("Upload a different sales CSV", type=["csv"])
    if uploaded is not None:
        raw_df = pd.read_csv(uploaded)
        raw_df["order_date"] = pd.to_datetime(raw_df["order_date"])
        raw_df["total_price"] = raw_df["price_after_discount"] * raw_df["product_count"]

# ============================================================
# GLOBAL DATE RANGE FILTER (applies to every section below)
# ============================================================
min_date = raw_df["order_date"].min().date()
max_date = raw_df["order_date"].max().date()

with st.sidebar:
    st.header("Filters")
    date_range = st.date_input(
        "Order date range",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date,
    )

    # date_input returns a single date until the user picks both ends
    if isinstance(date_range, tuple) and len(date_range) == 2:
        start_date, end_date = date_range
    else:
        start_date, end_date = min_date, max_date

    st.caption(f"Showing orders from **{start_date}** to **{end_date}**")

mask = (raw_df["order_date"].dt.date >= start_date) & (
    raw_df["order_date"].dt.date <= end_date
)
df = raw_df.loc[mask].copy()

if df.empty:
    st.warning("No orders in the selected date range. Pick a different range.")
    st.stop()

today = pd.Timestamp(end_date)  # "today" for recency calcs = end of selected range


# ============================================================
# CORE CUSTOMER SUMMARY (built once per filtered df, reused everywhere)
# ============================================================
@st.cache_data
def build_customer_summary(df: pd.DataFrame, today: pd.Timestamp) -> pd.DataFrame:
    cs = (
        df.groupby("customer_id")
        .agg(
            first_order_date=("order_date", "min"),
            last_order_date=("order_date", "max"),
            active_days=("order_date", lambda x: x.dt.date.nunique()),
            active_months=("order_date", lambda x: x.dt.to_period("M").nunique()),
            total_orders=("order_id", "nunique"),
            total_products=("product_count", "sum"),
            unique_products=("product_id", "nunique"),
            total_revenue=("total_price", "sum"),
            avg_order_value=("total_price", "mean"),
            avg_product_price=("price_after_discount", "mean"),
            total_discount=("product_discount", "sum"),
        )
        .reset_index()
    )

    cs["inactive_days"] = (today - cs["last_order_date"].dt.normalize()).dt.days
    cs["customer_age_days"] = (today - cs["first_order_date"].dt.normalize()).dt.days

    cs["customer_status"] = np.where(
        cs["inactive_days"] <= ACTIVE_DAYS_THRESHOLD, "Active", "Inactive"
    )
    cs["customer_type"] = np.where(
        cs["customer_age_days"] <= ACTIVE_DAYS_THRESHOLD, "New", "Old"
    )

    return cs.sort_values("total_revenue", ascending=False)


customer_summary = build_customer_summary(df, today)

day_bins = [0, 1, 3, 7, 30, 90, float("inf")]
day_labels = ["1 day", "2-3 days", "4-7 days", "8-30 days", "31-90 days", "90+ days"]

customer_summary["active_days_level"] = pd.cut(
    customer_summary["active_days"], bins=day_bins, labels=day_labels, include_lowest=True
)

inactive_bins = [-1, 0, 3, 7, 30, 90, float("inf")]
customer_summary["inactive_days_level"] = pd.cut(
    customer_summary["inactive_days"], bins=inactive_bins, labels=day_labels
)


# ============================================================
# KPI ROW
# ============================================================
st.header("Overview")

total_customers = customer_summary["customer_id"].nunique()
active_customers = (customer_summary["customer_status"] == "Active").sum()
inactive_customers = (customer_summary["customer_status"] == "Inactive").sum()
new_customers = (customer_summary["customer_type"] == "New").sum()
old_customers = (customer_summary["customer_type"] == "Old").sum()
total_revenue = customer_summary["total_revenue"].sum()
avg_customer_value = customer_summary["total_revenue"].mean()
avg_order_value = df["total_price"].mean()

kpi_cols = st.columns(4)
kpi_cols[0].metric("Total Customers", f"{total_customers:,}")
kpi_cols[1].metric("Active Customers", f"{active_customers:,}")
kpi_cols[2].metric("Inactive Customers", f"{inactive_customers:,}")
kpi_cols[3].metric("New Customers", f"{new_customers:,}")

kpi_cols2 = st.columns(4)
kpi_cols2[0].metric("Old Customers", f"{old_customers:,}")
kpi_cols2[1].metric("Total Revenue", f"₹{total_revenue:,.0f}")
kpi_cols2[2].metric("Avg Customer Value", f"₹{avg_customer_value:,.0f}")
kpi_cols2[3].metric("Avg Order Value", f"₹{avg_order_value:,.0f}")

st.divider()

# ============================================================
# TOP / BOTTOM CUSTOMERS
# ============================================================
st.header("Top & Bottom Customers")
col1, col2 = st.columns(2)
with col1:
    st.subheader("Top 10 by Revenue")
    st.dataframe(customer_summary.head(10), use_container_width=True)
with col2:
    st.subheader("Bottom 10 by Revenue")
    st.dataframe(customer_summary.tail(10), use_container_width=True)

st.divider()

# ============================================================
# ACTIVE / INACTIVE DAYS
# ============================================================
st.header("Customer Activity Levels")
col1, col2 = st.columns(2)

active_days_summary = (
    customer_summary.groupby("active_days_level", observed=True)
    .agg(total_customers=("customer_id", "nunique"))
    .reset_index()
)
inactive_days_summary = (
    customer_summary.groupby("inactive_days_level", observed=True)
    .agg(total_customers=("customer_id", "nunique"))
    .reset_index()
)

with col1:
    st.subheader("By Active Days")
    st.bar_chart(active_days_summary.set_index("active_days_level"))
with col2:
    st.subheader("By Inactive Days")
    st.bar_chart(inactive_days_summary.set_index("inactive_days_level"))

st.divider()

# ============================================================
# REVENUE SEGMENTATION
# ============================================================
st.header("Revenue Segmentation")

revenue_bins = [-np.inf, 1000, 5000, 10000, 50000, np.inf]
revenue_labels = ["< ₹1K", "₹1K - ₹5K", "₹5K - ₹10K", "₹10K - ₹50K", "₹50K+"]

customer_summary["revenue_segment"] = pd.cut(
    customer_summary["total_revenue"], bins=revenue_bins, labels=revenue_labels, include_lowest=True
)

revenue_segmentation = (
    customer_summary.groupby("revenue_segment", observed=True)
    .agg(
        total_customers=("customer_id", "nunique"),
        total_revenue=("total_revenue", "sum"),
        avg_customer_revenue=("total_revenue", "mean"),
        avg_orders=("total_orders", "mean"),
    )
    .reset_index()
)
revenue_segmentation["revenue_percentage"] = (
    revenue_segmentation["total_revenue"] / customer_summary["total_revenue"].sum() * 100
).round(2)

col1, col2 = st.columns([2, 1])
with col1:
    st.dataframe(revenue_segmentation, use_container_width=True)
with col2:
    st.bar_chart(revenue_segmentation.set_index("revenue_segment")["total_revenue"])

st.divider()

# ============================================================
# PRODUCT DIVERSITY
# ============================================================
st.header("Product Diversity")

product_bins = [0, 1, 3, 10, 20, np.inf]
product_labels = ["1 product", "2-3 products", "4-10 products", "11-20 products", "20+ products"]

customer_summary["product_diversity"] = pd.cut(
    customer_summary["unique_products"], bins=product_bins, labels=product_labels, include_lowest=True
)

product_diversity_summary = (
    customer_summary.groupby("product_diversity", observed=True)
    .agg(
        total_customers=("customer_id", "nunique"),
        total_revenue=("total_revenue", "sum"),
        avg_revenue=("total_revenue", "mean"),
        avg_orders=("total_orders", "mean"),
        avg_products=("unique_products", "mean"),
    )
    .reset_index()
)
product_diversity_summary["customer_percentage"] = (
    product_diversity_summary["total_customers"] / customer_summary["customer_id"].nunique() * 100
).round(2)

st.dataframe(product_diversity_summary, use_container_width=True)

st.divider()

# ============================================================
# RETENTION
# ============================================================
st.header("Customer Retention")

repeat_customers = (customer_summary["total_orders"] > 1).sum()
one_time_customers = (customer_summary["total_orders"] == 1).sum()
repeat_customer_rate = repeat_customers / total_customers * 100
one_time_customer_rate = one_time_customers / total_customers * 100

retention_summary = pd.DataFrame(
    {
        "metric": [
            "Total Customers",
            "Repeat Customers",
            "One-Time Customers",
            "Repeat Customer Rate %",
            "One-Time Customer Rate %",
        ],
        "value": [
            total_customers,
            repeat_customers,
            one_time_customers,
            round(repeat_customer_rate, 2),
            round(one_time_customer_rate, 2),
        ],
    }
)

col1, col2 = st.columns([1, 1])
with col1:
    st.dataframe(retention_summary, use_container_width=True, hide_index=True)
with col2:
    st.metric("Repeat Customer Rate", f"{repeat_customer_rate:.1f}%")
    st.metric("One-Time Customer Rate", f"{one_time_customer_rate:.1f}%")

st.divider()

# ============================================================
# REVENUE CONCENTRATION
# ============================================================
st.header("Revenue Concentration")

customer_rank = customer_summary.sort_values("total_revenue", ascending=False).reset_index(drop=True)
customer_rank["revenue_rank"] = customer_rank.index + 1
total_rev_for_conc = customer_rank["total_revenue"].sum()

concentration_results = []
for n in [10, 20, 50, 100]:
    n_actual = min(n, len(customer_rank))
    revenue = customer_rank.head(n_actual)["total_revenue"].sum()
    concentration_results.append(
        {
            "customer_group": f"Top {n}",
            "customers": n_actual,
            "revenue": revenue,
            "revenue_percentage": round(revenue / total_rev_for_conc * 100, 2),
        }
    )

for pct in [1, 5, 10]:
    n_actual = max(1, int(len(customer_rank) * pct / 100))
    revenue = customer_rank.head(n_actual)["total_revenue"].sum()
    concentration_results.append(
        {
            "customer_group": f"Top {pct}%",
            "customers": n_actual,
            "revenue": revenue,
            "revenue_percentage": round(revenue / total_rev_for_conc * 100, 2),
        }
    )

revenue_concentration = pd.DataFrame(concentration_results)

col1, col2 = st.columns([2, 1])
with col1:
    st.dataframe(revenue_concentration, use_container_width=True, hide_index=True)
with col2:
    st.bar_chart(revenue_concentration.set_index("customer_group")["revenue_percentage"])

st.divider()

# ============================================================
# ACTIVITY MATRIX
# ============================================================
st.header("Customer Activity Matrix")
st.caption("Active-day buckets vs. order-frequency buckets (customer counts)")

order_bins = [0, 1, 3, 10, 20, 30, np.inf]
order_labels = ["1 order", "2-3 orders", "4-10 orders", "11-20 orders", "21-30 orders", "30+ orders"]

customer_summary["order_frequency_level"] = pd.cut(
    customer_summary["total_orders"], bins=order_bins, labels=order_labels, include_lowest=True
)

activity_matrix = pd.crosstab(
    customer_summary["active_days_level"],
    customer_summary["order_frequency_level"],
)

st.dataframe(
    activity_matrix.style.background_gradient(cmap="Blues", axis=None),
    use_container_width=True,
)

st.divider()
st.caption(
    "All figures above reflect only orders placed between "
    f"{start_date} and {end_date}. Change the date range in the sidebar to update every section."
)