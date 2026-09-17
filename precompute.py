"""
Run this ONCE (or whenever the source data changes) to build all the summary
tables the dashboard needs, and save them as small CSV files.

Usage:
    python precompute.py                     # reads ./sales_date.csv
    python precompute.py path/to/file.csv    # reads a specific CSV

Outputs everything into ./precomputed/*.csv
"""
import sys
import os
import pandas as pd
import numpy as np

OUT_DIR = "precomputed"
os.makedirs(OUT_DIR, exist_ok=True)

import pandas as pd
from sqlalchemy import create_engine

from db_manager import load_env_file

load_env_file()

# MySQL connection
DB_HOST = os.environ.get("MYSQL_HOST", "localhost")
DB_PORT = os.environ.get("MYSQL_PORT", "3306")
DB_USER = os.environ.get("MYSQL_USER", "root")
DB_PASSWORD = os.environ.get("MYSQL_PASSWORD", "root123")
DB_NAME = os.environ.get("MYSQL_DATABASE", "farmora")

engine = create_engine(
    f"mysql+mysqlconnector://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

# Read only one MySQL table
query = "SELECT * FROM Order_Details"

df = pd.read_sql(query, engine)


df["order_date"] = pd.to_datetime(df["order_date"])
df["total_price"] = df["price_after_discount"] * df["product_count"]
df["day_of_week"] = df["order_date"].dt.day_name()
print(f"Loaded {len(df):,} rows.")

# ----------------------------------------------------------------------
# 1. PRODUCT SUMMARY
# ----------------------------------------------------------------------
product_summary = (
    df.groupby("product_id")
    .agg(
        total_orders=("order_id", "nunique"),
        total_quantity=("product_count", "sum"),
        total_revenue=("total_price", "sum"),
        avg_price=("product_price", "mean"),
        avg_discount=("product_discount", "mean"),
        unique_customers=("customer_id", "nunique"),
        avg_order_value=("total_price", "mean"),
    )
    .reset_index()
)
product_summary["revenue_per_customer"] = (
    product_summary["total_revenue"] / product_summary["unique_customers"]
)
product_summary["revenue_share_pct"] = (
    product_summary["total_revenue"] / product_summary["total_revenue"].sum() * 100
).round(2)
top_10_products = product_summary.sort_values("total_revenue", ascending=False).head(10)

product_summary.to_csv(f"{OUT_DIR}/product_summary.csv", index=False)
top_10_products.to_csv(f"{OUT_DIR}/top_10_products.csv", index=False)

# ----------------------------------------------------------------------
# 2. DAY OF WEEK REVENUE
# ----------------------------------------------------------------------
dow_order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
dow_revenue = (
    df.groupby("day_of_week")["total_price"]
    .agg(["sum", "mean", "count", "min", "max"])
    .reindex(dow_order)
    .reset_index()
)
dow_revenue.columns = [
    "day_of_week", "total_revenue", "avg_revenue", "transaction_count",
    "min_revenue", "max_revenue",
]
dow_revenue["pct_of_total"] = (
    dow_revenue["total_revenue"] / dow_revenue["total_revenue"].sum() * 100
).round(2)
dow_revenue.to_csv(f"{OUT_DIR}/dow_revenue.csv", index=False)

# ----------------------------------------------------------------------
# 3. MONTHLY REVENUE
# ----------------------------------------------------------------------
monthly_revenue = (
    df.groupby(df["order_date"].dt.to_period("M"))["total_price"]
    .agg(["sum", "mean", "count", "min", "max"])
    .reset_index()
)
monthly_revenue.columns = [
    "month", "total_revenue", "avg_revenue", "transaction_count",
    "min_revenue", "max_revenue",
]
monthly_revenue["month"] = monthly_revenue["month"].astype(str)
monthly_revenue["mom_growth_pct"] = monthly_revenue["total_revenue"].pct_change() * 100
monthly_revenue["cumulative_revenue"] = monthly_revenue["total_revenue"].cumsum()
monthly_revenue["pct_of_total"] = (
    monthly_revenue["total_revenue"] / monthly_revenue["total_revenue"].sum() * 100
).round(2)
monthly_revenue.to_csv(f"{OUT_DIR}/monthly_revenue.csv", index=False)

# ----------------------------------------------------------------------
# 4. DISCOUNT BUCKETING
# ----------------------------------------------------------------------
DISCOUNT_ORDER = ["0%", "1-5%", "6-10%", "11-20%", "21-30%", "30%+"]
bins = [-0.01, 0, 5, 10, 20, 30, np.inf]
df["discount_group"] = pd.cut(df["product_discount"], bins=bins, labels=DISCOUNT_ORDER)

discount_bucket_summary = (
    df.groupby("discount_group", observed=False)
    .agg(
        order_count=("order_id", "nunique"),
        total_qty=("product_count", "sum"),
        avg_qty=("product_count", "mean"),
        total_revenue=("total_price", "sum"),
        unique_customers=("customer_id", "nunique"),
    )
    .reindex(DISCOUNT_ORDER, fill_value=0)
    .reset_index()
)
discount_bucket_summary["revenue_share_pct"] = (
    discount_bucket_summary["total_revenue"] / discount_bucket_summary["total_revenue"].sum() * 100
).round(2)
discount_bucket_summary.to_csv(f"{OUT_DIR}/discount_bucket_summary.csv", index=False)

# ----------------------------------------------------------------------
# 5. RFM SEGMENTATION
# ----------------------------------------------------------------------
def safe_qcut_score(series, ascending_score=True, q=4):
    s = series.astype(float).copy()
    if not np.isfinite(s).all():
        finite_vals = s[np.isfinite(s)]
        fill_value = finite_vals.median() if len(finite_vals) else 0.0
        s = s.replace([np.inf, -np.inf], np.nan).fillna(fill_value)

    ranks = s.rank(method="first", ascending=True)
    pct = (ranks - 1) / max(len(s) - 1, 1)
    scores = np.floor(pct * q)
    scores = scores.clip(upper=q - 1) + 1
    scores = scores.fillna(1).astype(int)
    if not ascending_score:
        scores = (q + 1) - scores
    return scores

max_date = df["order_date"].max()
rfm = df.groupby("customer_id").agg(
    recency=("order_date", lambda x: (max_date - x.max()).days),
    frequency=("order_id", "nunique"),
    monetary=("total_price", "sum"),
).reset_index()

rfm["R_score"] = safe_qcut_score(rfm["recency"], ascending_score=False)
rfm["F_score"] = safe_qcut_score(rfm["frequency"], ascending_score=True)
rfm["M_score"] = safe_qcut_score(rfm["monetary"], ascending_score=True)
rfm["RFM_score"] = rfm["R_score"].astype(str) + rfm["F_score"].astype(str) + rfm["M_score"].astype(str)

r, f, m = rfm["R_score"], rfm["F_score"], rfm["M_score"]
conditions = [
    (r >= 4) & (f >= 4) & (m >= 4),
    (r >= 3) & (f >= 3),
    (r >= 4) & (f <= 2),
    (r == 3) & (f <= 2),
    (r <= 2) & (f >= 3) & (m >= 3),
    (r <= 2) & (f <= 2) & (m >= 3),
    (r <= 2) & (f <= 2) & (m <= 2),
]
choices = [
    "Champions", "Loyal Customers", "New Customers", "Potential Loyalist",
    "At Risk", "Can't Lose Them", "Lost",
]
rfm["segment"] = np.select(conditions, choices, default="Needs Attention")

segment_summary = (
    rfm.groupby("segment")
    .agg(
        customer_count=("customer_id", "count"),
        avg_recency=("recency", "mean"),
        avg_frequency=("frequency", "mean"),
        avg_monetary=("monetary", "mean"),
        total_revenue=("monetary", "sum"),
    )
    .sort_values("total_revenue", ascending=False)
    .reset_index()
)
rfm.to_csv(f"{OUT_DIR}/rfm.csv", index=False)
segment_summary.to_csv(f"{OUT_DIR}/segment_summary.csv", index=False)

# ----------------------------------------------------------------------
# 6. NEW vs RETURNING CUSTOMERS
# ----------------------------------------------------------------------
first_orders = df.groupby("customer_id")["order_date"].min().reset_index()
first_orders.columns = ["customer_id", "first_order_date"]
df = df.merge(first_orders, on="customer_id")
df["customer_type"] = np.where(df["order_date"] == df["first_order_date"], "New", "Returning")

customer_type_summary = (
    df.groupby("customer_type")
    .agg(
        total_revenue=("total_price", "sum"),
        order_count=("order_id", "nunique"),
        unique_customers=("customer_id", "nunique"),
    )
    .reset_index()
)
customer_type_summary["pct_of_total_revenue"] = (
    customer_type_summary["total_revenue"] / customer_type_summary["total_revenue"].sum() * 100
).round(2)
customer_type_summary["pct_of_total_orders"] = (
    customer_type_summary["order_count"] / customer_type_summary["order_count"].sum() * 100
).round(2)
customer_type_summary["pct_of_total_customers"] = (
    customer_type_summary["unique_customers"] / customer_type_summary["unique_customers"].sum() * 100
).round(2)
customer_type_summary["revenue_per_customer"] = (
    customer_type_summary["total_revenue"] / customer_type_summary["unique_customers"]
).round(2)
customer_type_summary.to_csv(f"{OUT_DIR}/customer_type_summary.csv", index=False)

# ----------------------------------------------------------------------
# 7. ORDER COUNT BUCKETING
# ----------------------------------------------------------------------
orders_per_customer = df.groupby("customer_id")["order_id"].nunique()
customer_revenue = df.groupby("customer_id")["total_price"].sum()
total_customers = df["customer_id"].nunique()

BUCKET_ORDER = ["1 (one-time)", "2", "3-5", "6-10", "10+"]
bins = [0, 1, 2, 5, 10, np.inf]
order_bucket = pd.cut(orders_per_customer, bins=bins, labels=BUCKET_ORDER)

order_bucket_distribution = (
    order_bucket.value_counts()
    .reindex(BUCKET_ORDER)
    .fillna(0)
    .astype(int)
    .reset_index()
)
order_bucket_distribution.columns = ["order_bucket", "num_customers"]
order_bucket_distribution["pct_of_customers"] = (
    order_bucket_distribution["num_customers"] / total_customers * 100
).round(2)

bucket_revenue = customer_revenue.groupby(order_bucket, observed=False).sum().reindex(BUCKET_ORDER).fillna(0)
order_bucket_distribution["total_revenue"] = bucket_revenue.values.round(2)
order_bucket_distribution["pct_of_revenue"] = (
    order_bucket_distribution["total_revenue"] / order_bucket_distribution["total_revenue"].sum() * 100
).round(2)
order_bucket_distribution.to_csv(f"{OUT_DIR}/order_bucket_distribution.csv", index=False)

# ----------------------------------------------------------------------
# 8. OVERVIEW KPIs (small file, avoids touching raw df in the dashboard)
# ----------------------------------------------------------------------
kpis = pd.DataFrame([{
    "total_revenue": df["total_price"].sum(),
    "total_orders": df["order_id"].nunique(),
    "unique_customers": df["customer_id"].nunique(),
    "unique_products": df["product_id"].nunique(),
    "avg_order_value": df["total_price"].mean(),
}])
kpis.to_csv(f"{OUT_DIR}/kpis.csv", index=False)

print(f"\nDone. Wrote 9 CSV files to ./{OUT_DIR}/")
for f in sorted(os.listdir(OUT_DIR)):
    print(f"  - {OUT_DIR}/{f}")


# ----------------------------------------------------------------------
# 8. CUSTOMER ANALYTICS
# ----------------------------------------------------------------------

print("Creating customer analytics...")

# =========================
# CUSTOMER SUMMARY
# =========================

customer_summary = (
    df.groupby("customer_id")
    .agg(
        first_order_date=("order_date", "min"),
        last_order_date=("order_date", "max"),
        active_days=("order_date", lambda x: x.dt.normalize().nunique()),
        total_orders=("order_id", "nunique"),
        total_products=("product_count", "sum"),
        unique_products=("product_id", "nunique"),
        total_revenue=("total_price", "sum"),
        avg_order_value=("total_price", "mean")
    )
    .reset_index()
)


# =========================
# CUSTOMER STATUS
# =========================

today = df["order_date"].max()

customer_summary["inactive_days"] = (
    today - customer_summary["last_order_date"]
).dt.days

# Customer lifetime days
customer_summary["customer_lifetime_days"] = (
    today - customer_summary["first_order_date"]
).dt.days

customer_summary["status"] = np.where(
    customer_summary["inactive_days"] <= 30,
    "Active",
    "Inactive"
)


# Save complete customer summary
customer_summary.to_csv(
    f"{OUT_DIR}/customer_summary.csv",
    index=False
)


# =========================
# TOP 10 CUSTOMERS
# =========================

top_10_customers = (
    customer_summary
    .sort_values("total_revenue", ascending=False)
    .head(10)
)

top_10_customers.to_csv(
    f"{OUT_DIR}/top_10_customers.csv",
    index=False
)


# =========================
# INACTIVE DAYS BUCKETING
# =========================

def inactive_days_bucket(days):

    if days == 0:
        return "0 days"

    elif 1 <= days <= 3:
        return "1-3 days"

    elif 4 <= days <= 7:
        return "4-7 days"

    elif 8 <= days <= 30:
        return "8-30 days"

    elif 31 <= days <= 90:
        return "31-90 days"

    else:
        return "90+ days"


INACTIVE_DAYS_ORDER = [
    "0 days",
    "1-3 days",
    "4-7 days",
    "8-30 days",
    "31-90 days",
    "90+ days"
]


customer_summary["inactive_days_group"] = (
    customer_summary["inactive_days"]
    .apply(inactive_days_bucket)
)


inactive_days_summary = (
    customer_summary
    .groupby("inactive_days_group", observed=False)
    .agg(
        customer_count=("customer_id", "count"),
        total_revenue=("total_revenue", "sum")
    )
    .reindex(INACTIVE_DAYS_ORDER, fill_value=0)
    .reset_index()
)


inactive_days_summary["customer_pct"] = (
    inactive_days_summary["customer_count"]
    / inactive_days_summary["customer_count"].sum()
    * 100
).round(2)


inactive_days_summary["revenue_pct"] = (
    inactive_days_summary["total_revenue"]
    / inactive_days_summary["total_revenue"].sum()
    * 100
).round(2)


inactive_days_summary.to_csv(
    f"{OUT_DIR}/inactive_days_summary.csv",
    index=False
)


# =========================
# LAST 30 DAYS ACTIVITY
# =========================

last_30_days_df = df[
    df["order_date"] >= (today - pd.Timedelta(days=30))
]


customer_activity = (
    last_30_days_df
    .groupby("customer_id")
    .agg(
        days_present_last_30=(
            "order_date",
            lambda x: x.dt.normalize().nunique()
        ),
        orders_last_30=(
            "order_id",
            "nunique"
        ),
        revenue_last_30=(
            "total_price",
            "sum"
        )
    )
    .reset_index()
)


# =========================
# MERGE CUSTOMER ACTIVITY
# =========================

customer_summary = customer_summary.merge(
    customer_activity,
    on="customer_id",
    how="left"
)


customer_summary["days_present_last_30"] = (
    customer_summary["days_present_last_30"]
    .fillna(0)
    .astype(int)
)

customer_summary["orders_last_30"] = (
    customer_summary["orders_last_30"]
    .fillna(0)
    .astype(int)
)

customer_summary["revenue_last_30"] = (
    customer_summary["revenue_last_30"]
    .fillna(0)
)


# Save updated customer summary again
customer_summary.to_csv(
    f"{OUT_DIR}/customer_summary.csv",
    index=False
)


# =========================
# ACTIVE DAYS BUCKETING
# =========================

def active_days_bucket(days):

    if days <= 3:
        return "1-3 days"

    elif 4 <= days <= 7:
        return "4-7 days"

    else:
        return "8-30 days"


ACTIVE_DAYS_ORDER = [
    "1-3 days",
    "4-7 days",
    "8-30 days"
]


customer_summary["active_days_group"] = (
    customer_summary["days_present_last_30"]
    .apply(active_days_bucket)
)


active_days_summary = (
    customer_summary
    .groupby("active_days_group", observed=False)
    .agg(
        customer_count=("customer_id", "count"),
        total_revenue=("revenue_last_30", "sum"),
        total_orders=("orders_last_30", "sum")
    )
    .reindex(ACTIVE_DAYS_ORDER, fill_value=0)
    .reset_index()
)


active_days_summary["customer_pct"] = (
    active_days_summary["customer_count"]
    / active_days_summary["customer_count"].sum()
    * 100
).round(2)


active_days_summary["revenue_pct"] = (
    active_days_summary["total_revenue"]
    / active_days_summary["total_revenue"].sum()
    * 100
).round(2)


active_days_summary.to_csv(
    f"{OUT_DIR}/active_days_summary.csv",
    index=False
)


print("Customer analytics completed.")