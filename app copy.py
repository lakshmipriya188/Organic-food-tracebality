import os

import altair as alt
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st


# ============================================================================
# PAGE CONFIGURATION
# ============================================================================

st.set_page_config(  page_title="Sales Analytics Dashboard",
    page_icon="📊", layout="wide", )

st.title("📊 Sales Analytics Dashboard")
st.caption("Product, time, discount, customer, and RFM analysis")


# ============================================================================
# GLOBAL CONFIGURATION
# ============================================================================

PRECOMPUTED_DIR = "precomputed"
CHART_TEMPLATE = "plotly_white"


# ============================================================================
# LOAD PRECOMPUTED DATA
#
# All calculations are performed in precompute.py.
# Streamlit only reads the already-created CSV summary files.
# ============================================================================

@st.cache_data
def load_precomputed(path):
    """Load a precomputed CSV file."""
    return pd.read_csv(path)


# ============================================================================
# CHECK PRECOMPUTED DIRECTORY
# ============================================================================

if not os.path.isdir(PRECOMPUTED_DIR):
    st.error(
        f"Couldn't find the `{PRECOMPUTED_DIR}/` folder.\n\n"
        "Run `python precompute.py` first to generate the summary CSV files."
    )
    st.stop()


# ============================================================================
# PRECOMPUTED FILES
# ============================================================================

FILES = {
    # ------------------------------------------------------------------------
    # General Analytics
    # ------------------------------------------------------------------------
    "kpis": "kpis.csv",
    "top_10_products": "top_10_products.csv",
    "product_summary": "product_summary.csv",
    "dow_revenue": "dow_revenue.csv",
    "monthly_revenue": "monthly_revenue.csv",
    "discount_bucket_summary": "discount_bucket_summary.csv",
    "rfm": "rfm.csv",
    "segment_summary": "segment_summary.csv",
    "customer_type_summary": "customer_type_summary.csv",
    "order_bucket_distribution": "order_bucket_distribution.csv",

    # ------------------------------------------------------------------------
    # Customer Analytics
    # ------------------------------------------------------------------------
    "customer_summary": "customer_summary.csv",
    "top_customers": "top_10_customers.csv",
    "inactive_days_summary": "inactive_days_summary.csv",
    "active_days_summary": "active_days_summary.csv",
}


# ============================================================================
# CHECK FOR MISSING FILES
# ============================================================================

missing_files = [
    filename
    for filename in FILES.values()
    if not os.path.exists(os.path.join(PRECOMPUTED_DIR, filename))
]

if missing_files:
    st.error(
        "The following precomputed file(s) are missing:\n\n"
        + "\n".join(f"- {file}" for file in missing_files)
        + "\n\n"
        "Run `python precompute.py` again to regenerate them."
    )
    st.stop()


# ============================================================================
# LOAD ALL PRECOMPUTED TABLES
# ============================================================================

tables = {
    name: load_precomputed(
        os.path.join(PRECOMPUTED_DIR, filename)
    )
    for name, filename in FILES.items()
}


# ============================================================================
# SORT / CATEGORICAL ORDERS
# ============================================================================

# ----------------------------------------------------------------------------
# Discount Bucket Order
# ----------------------------------------------------------------------------

DISCOUNT_ORDER = [
    "0%",
    "1-5%",
    "6-10%",
    "11-20%",
    "21-30%",
    "30%+",
]

tables["discount_bucket_summary"]["discount_group"] = pd.Categorical(
    tables["discount_bucket_summary"]["discount_group"],
    categories=DISCOUNT_ORDER,
    ordered=True,
)

tables["discount_bucket_summary"] = (
    tables["discount_bucket_summary"]
    .sort_values("discount_group")
)


# ----------------------------------------------------------------------------
# Order Frequency Bucket Order
# ----------------------------------------------------------------------------

ORDER_BUCKET_ORDER = [
    "1 (one-time)",
    "2",
    "3-5",
    "6-10",
    "10+",
]

tables["order_bucket_distribution"]["order_bucket"] = pd.Categorical(
    tables["order_bucket_distribution"]["order_bucket"],
    categories=ORDER_BUCKET_ORDER,
    ordered=True,
)

tables["order_bucket_distribution"] = (
    tables["order_bucket_distribution"]
    .sort_values("order_bucket")
)


# ----------------------------------------------------------------------------
# Day-of-Week Order
# ----------------------------------------------------------------------------

DOW_ORDER = [
    "Monday",
    "Tuesday",
    "Wednesday",
    "Thursday",
    "Friday",
    "Saturday",
    "Sunday",
]

tables["dow_revenue"]["day_of_week"] = pd.Categorical(
    tables["dow_revenue"]["day_of_week"],
    categories=DOW_ORDER,
    ordered=True,
)

tables["dow_revenue"] = (
    tables["dow_revenue"]
    .sort_values("day_of_week")
)


# ----------------------------------------------------------------------------
# Inactive Days Order
# ----------------------------------------------------------------------------

INACTIVE_DAYS_ORDER = [
    "0 days",
    "1-3 days",
    "4-7 days",
    "8-30 days",
    "31-90 days",
    "90+ days",
]

tables["inactive_days_summary"]["inactive_days_group"] = pd.Categorical(
    tables["inactive_days_summary"]["inactive_days_group"],
    categories=INACTIVE_DAYS_ORDER,
    ordered=True,
)

tables["inactive_days_summary"] = (
    tables["inactive_days_summary"]
    .sort_values("inactive_days_group")
)


# ----------------------------------------------------------------------------
# Active Days Order
# ----------------------------------------------------------------------------

ACTIVE_DAYS_ORDER = [
    "1-3 days",
    "4-7 days",
    "8-30 days",
]

tables["active_days_summary"]["active_days_group"] = pd.Categorical(
    tables["active_days_summary"]["active_days_group"],
    categories=ACTIVE_DAYS_ORDER,
    ordered=True,
)

tables["active_days_summary"] = (
    tables["active_days_summary"]
    .sort_values("active_days_group")
)


# ============================================================================
# SIDEBAR NAVIGATION
# ============================================================================

with st.sidebar:
    st.header("Navigate")

    section = st.radio(
        "Go to section",
        [
            "Overview",
            "Customer Performance",
            "Product Performance",
            "Day-of-Week Trends",
            "Monthly Revenue Trend",
            "Discount Analysis",
            "RFM Segmentation",
            "New vs Returning Customers",
            "Order Frequency Buckets",
        ],
    )


# ============================================================================
# HELPER FUNCTION
# ============================================================================

def kpi_row(items):
    """Display multiple KPI metrics in a single row."""

    columns = st.columns(len(items))

    for column, (label, value) in zip(columns, items):
        column.metric(label, value)


# ============================================================================
# SECTION: OVERVIEW
# ============================================================================

if section == "Overview":

    kpis = tables["kpis"]
    monthly_revenue = tables["monthly_revenue"]
    customer_type_summary = tables["customer_type_summary"]

    # ------------------------------------------------------------------------
    # Header
    # ------------------------------------------------------------------------

    st.subheader("📊 Overview")

    # ------------------------------------------------------------------------
    # KPI Row
    # ------------------------------------------------------------------------

    kpi = kpis.iloc[0]

    kpi_row(
        [
            (
                "Total Revenue",
                f"₹{kpi['total_revenue']:,.0f}",
            ),
            (
                "Total Orders",
                f"{int(kpi['total_orders']):,}",
            ),
            (
                "Unique Customers",
                f"{int(kpi['unique_customers']):,}",
            ),
            (
                "Unique Products",
                f"{int(kpi['unique_products']):,}",
            ),
            (
                "Avg Order Value",
                f"₹{kpi['avg_order_value']:,.2f}",
            ),
        ]
    )

    st.divider()

    # ------------------------------------------------------------------------
    # Charts
    # ------------------------------------------------------------------------

    col1, col2 = st.columns(2)

    with col1:

        fig = px.line(
            monthly_revenue,
            x="month",
            y="total_revenue",
            markers=True,
            title="Monthly Revenue Trend",
            template=CHART_TEMPLATE,
        )

        fig.update_layout(
            xaxis_title="Month",
            yaxis_title="Revenue",
        )

        st.plotly_chart(
            fig,
            use_container_width=True,
        )

    with col2:

        fig = px.pie(
            customer_type_summary,
            names="customer_type",
            values="total_revenue",
            title="Revenue Split: New vs Returning",
            hole=0.45,
            template=CHART_TEMPLATE,
        )

        st.plotly_chart(
            fig,
            use_container_width=True,
        )

    st.info(
        "Use the sidebar to explore Customer, Product, "
        "Revenue, Discount, RFM, and Order Frequency analysis."
    )


# ============================================================================
# SECTION: CUSTOMER PERFORMANCE
# ============================================================================

elif section == "Customer Performance":

    customer_summary = tables["customer_summary"]
    top_customers = tables["top_customers"]
    inactive_days_summary = tables["inactive_days_summary"]
    active_days_summary = tables["active_days_summary"]

    # ========================================================================
    # CUSTOMER OVERVIEW
    # ========================================================================

    st.subheader("👥 Customer Overview")

    # ------------------------------------------------------------------------
    # Customer KPIs
    # ------------------------------------------------------------------------

    total_customers = (
        customer_summary["customer_id"]
        .nunique()
    )

    active_customers = (
        customer_summary["status"]
        .eq("Active")
        .sum()
    )

    inactive_customers = (
        customer_summary["status"]
        .eq("Inactive")
        .sum()
    )

    total_revenue = (
        customer_summary["total_revenue"]
        .sum()
    )

    avg_customer_value = (
        customer_summary["total_revenue"]
        .mean()
    )

    avg_order_value = (
        customer_summary["avg_order_value"]
        .mean()
    )

    total_orders = (
        customer_summary["total_orders"]
        .sum()
    )

    # ------------------------------------------------------------------------
    # First KPI Row
    # ------------------------------------------------------------------------

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "Total Customers",
        f"{total_customers:,}",
    )

    col2.metric(
        "Active Customers",
        f"{active_customers:,}",
    )

    col3.metric(
        "Inactive Customers",
        f"{inactive_customers:,}",
    )

    col4.metric(
        "Total Revenue",
        f"₹{total_revenue:,.0f}",
    )

    # ------------------------------------------------------------------------
    # Second KPI Row
    # ------------------------------------------------------------------------

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Avg Customer Value",
        f"₹{avg_customer_value:,.0f}",
    )

    col2.metric(
        "Avg Order Value",
        f"₹{avg_order_value:,.0f}",
    )

    col3.metric(
        "Total Orders",
        f"{total_orders:,}",
    )

    st.divider()

    # ========================================================================
    # TOP 10 CUSTOMERS
    # ========================================================================

    st.subheader("🏆 Top 10 Customers")

    st.dataframe(
        top_customers,
        use_container_width=True,
        hide_index=True,
    )

    st.divider()

    # ========================================================================
    # INACTIVE DAYS DISTRIBUTION
    # ========================================================================

    st.subheader("📉 Inactive Days Distribution")

    inactive_chart = (
        alt.Chart(inactive_days_summary)
        .mark_bar()
        .encode(
            x=alt.X(
                "inactive_days_group:N",
                sort=INACTIVE_DAYS_ORDER,
                title="Inactive Days Group",
            ),
            y=alt.Y(
                "customer_count:Q",
                title="Customers",
            ),
            tooltip=[
                alt.Tooltip(
                    "inactive_days_group:N",
                    title="Inactive Days",
                ),
                alt.Tooltip(
                    "customer_count:Q",
                    title="Customers",
                ),
                alt.Tooltip(
                    "customer_pct:Q",
                    title="Customer %",
                    format=".2f",
                ),
                alt.Tooltip(
                    "total_revenue:Q",
                    title="Revenue",
                    format=",.0f",
                ),
                alt.Tooltip(
                    "revenue_pct:Q",
                    title="Revenue %",
                    format=".2f",
                ),
            ],
        )
        .properties(
            height=400,
        )
    )

    st.altair_chart(
        inactive_chart,
        use_container_width=True,
    )

    st.divider()

    # ========================================================================
    # ACTIVE DAYS DISTRIBUTION - LAST 30 DAYS
    # ========================================================================

    st.subheader(
        "📈 Active Days Distribution — Last 30 Days"
    )

    base = alt.Chart(
        active_days_summary
    ).encode(
        x=alt.X(
            "active_days_group:N",
            sort=ACTIVE_DAYS_ORDER,
            title="Active Days Group",
        )
    )

    # ------------------------------------------------------------------------
    # Revenue Line
    # ------------------------------------------------------------------------

    line_revenue = (
        base
        .mark_line(
            point=True,
            strokeWidth=3,
        )
        .encode(
            y=alt.Y(
                "total_revenue:Q",
                axis=alt.Axis(
                    title="Total Revenue",
                ),
            ),
            tooltip=[
                alt.Tooltip(
                    "active_days_group:N",
                    title="Active Days",
                ),
                alt.Tooltip(
                    "total_revenue:Q",
                    title="Revenue",
                    format=",.0f",
                ),
                alt.Tooltip(
                    "revenue_pct:Q",
                    title="Revenue %",
                    format=".2f",
                ),
            ],
        )
    )

    # ------------------------------------------------------------------------
    # Customer Count Line
    # ------------------------------------------------------------------------

    line_customers = (
        base
        .mark_line(
            point=True,
            strokeWidth=3,
        )
        .encode(
            y=alt.Y(
                "customer_count:Q",
                axis=alt.Axis(
                    title="Customer Count",
                    orient="right",
                ),
            ),
            tooltip=[
                alt.Tooltip(
                    "active_days_group:N",
                    title="Active Days",
                ),
                alt.Tooltip(
                    "customer_count:Q",
                    title="Customers",
                ),
                alt.Tooltip(
                    "customer_pct:Q",
                    title="Customer %",
                    format=".2f",
                ),
            ],
        )
    )

    # ------------------------------------------------------------------------
    # Combined Chart
    # ------------------------------------------------------------------------

    combo_chart = (
        alt.layer(
            line_revenue,
            line_customers,
        )
        .resolve_scale(
            y="independent",
        )
        .properties(
            height=450,
        )
    )

    st.altair_chart(
        combo_chart,
        use_container_width=True,
    )

    st.divider()

    # ========================================================================
    # COMPLETE CUSTOMER SUMMARY
    # ========================================================================

    with st.expander("View Complete Customer Summary"):

        st.dataframe(
            customer_summary,
            use_container_width=True,
            hide_index=True,
        )


# ============================================================================
# SECTION: PRODUCT PERFORMANCE
# ============================================================================

elif section == "Product Performance":

    top_10_products = tables["top_10_products"]
    product_summary = tables["product_summary"]

    st.subheader("🏆 Top 10 Products by Revenue")

    # ------------------------------------------------------------------------
    # Top 10 Products
    # ------------------------------------------------------------------------

    fig = px.bar(
        top_10_products.sort_values(
            "total_revenue"
        ),
        x="total_revenue",
        y="product_id",
        orientation="h",
        color="revenue_share_pct",
        color_continuous_scale="Blues",
        text="total_revenue",
        template=CHART_TEMPLATE,
        labels={
            "total_revenue": "Total Revenue",
            "product_id": "Product ID",
        },
    )

    fig.update_traces(
        texttemplate="₹%{text:,.0f}",
        textposition="outside",
    )

    # Uncomment if you want the bar chart displayed:
    # st.plotly_chart(fig, use_container_width=True)

    # ------------------------------------------------------------------------
    # Product Analysis
    # ------------------------------------------------------------------------

    col1, col2 = st.columns(2)

    with col1:

        fig2 = px.treemap(
            top_10_products,
            path=["product_id"],
            values="total_revenue",
            color="avg_discount",
            color_continuous_scale="RdYlGn_r",
            title=(
                "Revenue Share of Top 10 Products "
                "(size = revenue, color = avg discount)"
            ),
            template=CHART_TEMPLATE,
        )

        st.plotly_chart(
            fig2,
            use_container_width=True,
        )

    with col2:

        fig3 = px.scatter(
            product_summary,
            x="avg_price",
            y="total_quantity",
            size="total_revenue",
            color="revenue_share_pct",
            hover_name="product_id",
            title=(
                "Price vs Quantity Sold "
                "(bubble = revenue)"
            ),
            template=CHART_TEMPLATE,
            color_continuous_scale="Viridis",
        )

        st.plotly_chart(
            fig3,
            use_container_width=True,
        )

    # ------------------------------------------------------------------------
    # Product Table
    # ------------------------------------------------------------------------

    st.dataframe(
        top_10_products,
        use_container_width=True,
        hide_index=True,
    )


# ============================================================================
# SECTION: DAY OF WEEK
# ============================================================================

elif section == "Day-of-Week Trends":

    dow_revenue = tables["dow_revenue"]

    st.subheader("📅 Revenue by Day of Week")

    # ------------------------------------------------------------------------
    # Radar Chart
    # ------------------------------------------------------------------------

    fig = px.line_polar(
        dow_revenue,
        r="total_revenue",
        theta="day_of_week",
        line_close=True,
        title="Revenue by Day of Week",
        template=CHART_TEMPLATE,
    )

    fig.update_traces(
        fill="toself"
    )

    st.plotly_chart(
        fig,
        use_container_width=True,
    )

    # ------------------------------------------------------------------------
    # Day Analysis
    # ------------------------------------------------------------------------

    col1, col2 = st.columns(2)

    with col1:

        fig2 = px.bar(
            dow_revenue,
            x="day_of_week",
            y="transaction_count",
            color="avg_revenue",
            color_continuous_scale="Teal",
            title="Transaction Count by Day",
            template=CHART_TEMPLATE,
        )

        st.plotly_chart(
            fig2,
            use_container_width=True,
        )

    with col2:

        fig3 = px.funnel(
            dow_revenue.sort_values(
                "total_revenue",
                ascending=False,
            ),
            x="total_revenue",
            y="day_of_week",
            title="Days Ranked by Total Revenue",
            template=CHART_TEMPLATE,
        )

        st.plotly_chart(
            fig3,
            use_container_width=True,
        )

    # ------------------------------------------------------------------------
    # Data Table
    # ------------------------------------------------------------------------

    st.dataframe(
        dow_revenue,
        use_container_width=True,
        hide_index=True,
    )


# ============================================================================
# SECTION: MONTHLY REVENUE
# ============================================================================

elif section == "Monthly Revenue Trend":

    monthly_revenue = tables["monthly_revenue"]

    st.subheader("📈 Monthly Revenue")

    # ------------------------------------------------------------------------
    # Monthly Revenue + Cumulative Revenue
    # ------------------------------------------------------------------------

    fig = go.Figure()

    fig.add_trace(
        go.Bar(
            x=monthly_revenue["month"],
            y=monthly_revenue["total_revenue"],
            name="Monthly Revenue",
        )
    )

    fig.add_trace(
        go.Scatter(
            x=monthly_revenue["month"],
            y=monthly_revenue["cumulative_revenue"],
            name="Cumulative Revenue",
            yaxis="y2",
            mode="lines+markers",
        )
    )

    fig.update_layout(
        title="Monthly Revenue with Cumulative Overlay",
        yaxis=dict(
            title="Monthly Revenue"
        ),
        yaxis2=dict(
            title="Cumulative Revenue",
            overlaying="y",
            side="right",
        ),
        template=CHART_TEMPLATE,
    )

    st.plotly_chart(
        fig,
        use_container_width=True,
    )

    # ------------------------------------------------------------------------
    # Monthly Analysis
    # ------------------------------------------------------------------------

    col1, col2 = st.columns(2)

    with col1:

        fig2 = px.bar(
            monthly_revenue,
            x="month",
            y="mom_growth_pct",
            color="mom_growth_pct",
            color_continuous_scale="RdYlGn",
            title="Month-over-Month Growth %",
            template=CHART_TEMPLATE,
        )

        st.plotly_chart(
            fig2,
            use_container_width=True,
        )

    with col2:

        fig3 = px.area(
            monthly_revenue,
            x="month",
            y="pct_of_total",
            title="Share of Total Revenue by Month",
            template=CHART_TEMPLATE,
        )

        st.plotly_chart(
            fig3,
            use_container_width=True,
        )

    # ------------------------------------------------------------------------
    # Data Table
    # ------------------------------------------------------------------------

    st.dataframe(
        monthly_revenue,
        use_container_width=True,
        hide_index=True,
    )


# ============================================================================
# SECTION: DISCOUNT ANALYSIS
# ============================================================================

elif section == "Discount Analysis":

    discount_bucket_summary = tables[
        "discount_bucket_summary"
    ]

    st.subheader("🏷️ Discount Bucket Analysis")

    # ------------------------------------------------------------------------
    # Revenue by Discount
    # ------------------------------------------------------------------------

    fig = px.bar(
        discount_bucket_summary,
        x="discount_group",
        y="total_revenue",
        color="revenue_share_pct",
        color_continuous_scale="Sunset",
        title="Revenue by Discount Bucket",
        template=CHART_TEMPLATE,
    )

    st.plotly_chart(
        fig,
        use_container_width=True,
    )

    # ------------------------------------------------------------------------
    # Discount Analysis
    # ------------------------------------------------------------------------

    col1, col2 = st.columns(2)

    with col1:

        fig2 = px.pie(
            discount_bucket_summary,
            names="discount_group",
            values="total_qty",
            title="Quantity Sold Share by Discount Bucket",
            template=CHART_TEMPLATE,
        )

        st.plotly_chart(
            fig2,
            use_container_width=True,
        )

    with col2:

        fig3 = px.scatter(
            discount_bucket_summary,
            x="avg_qty",
            y="unique_customers",
            size="total_revenue",
            color="discount_group",
            title=(
                "Avg Qty vs Unique Customers "
                "by Discount Bucket"
            ),
            template=CHART_TEMPLATE,
        )

        st.plotly_chart(
            fig3,
            use_container_width=True,
        )

    # ------------------------------------------------------------------------
    # Data Table
    # ------------------------------------------------------------------------

    st.dataframe(
        discount_bucket_summary,
        use_container_width=True,
        hide_index=True,
    )


# ============================================================================
# SECTION: RFM SEGMENTATION
# ============================================================================

elif section == "RFM Segmentation":

    rfm = tables["rfm"]
    segment_summary = tables["segment_summary"]

    st.subheader("👥 RFM Customer Segmentation")

    # ------------------------------------------------------------------------
    # Segment Treemap
    # ------------------------------------------------------------------------

    fig = px.treemap(
        segment_summary,
        path=["segment"],
        values="customer_count",
        color="total_revenue",
        color_continuous_scale="Blues",
        title=(
            "Customer Segments "
            "(size = customers, color = revenue)"
        ),
        template=CHART_TEMPLATE,
    )

    st.plotly_chart(
        fig,
        use_container_width=True,
    )

    # ------------------------------------------------------------------------
    # Segment Analysis
    # ------------------------------------------------------------------------

    col1, col2 = st.columns(2)

    with col1:

        fig2 = px.bar(
            segment_summary.sort_values(
                "total_revenue"
            ),
            x="total_revenue",
            y="segment",
            orientation="h",
            title="Total Revenue by Segment",
            template=CHART_TEMPLATE,
        )

        st.plotly_chart(
            fig2,
            use_container_width=True,
        )

    with col2:

        fig3 = px.scatter_3d(
            rfm,
            x="R_score",
            y="F_score",
            z="M_score",
            color="segment",
            opacity=0.7,
            title="RFM Score Cube",
            template=CHART_TEMPLATE,
        )

        st.plotly_chart(
            fig3,
            use_container_width=True,
        )

    # ------------------------------------------------------------------------
    # Segment Summary
    # ------------------------------------------------------------------------

    st.dataframe(
        segment_summary,
        use_container_width=True,
        hide_index=True,
    )

    # ------------------------------------------------------------------------
    # Raw RFM
    # ------------------------------------------------------------------------

    with st.expander(
        "View Raw RFM Table"
    ):

        st.dataframe(
            rfm,
            use_container_width=True,
            hide_index=True,
        )


# ============================================================================
# SECTION: NEW VS RETURNING CUSTOMERS
# ============================================================================

elif section == "New vs Returning Customers":

    customer_type_summary = tables[
        "customer_type_summary"
    ]

    st.subheader(
        "🔁 New vs Returning Customers"
    )

    # ------------------------------------------------------------------------
    # Customer Count and Revenue per Customer
    # ------------------------------------------------------------------------

    col1, col2 = st.columns(2)

    with col1:

        fig = px.pie(
            customer_type_summary,
            names="customer_type",
            values="unique_customers",
            title="Customer Count Split",
            hole=0.4,
            template=CHART_TEMPLATE,
        )

        st.plotly_chart(
            fig,
            use_container_width=True,
        )

    with col2:

        fig2 = px.bar(
            customer_type_summary,
            x="customer_type",
            y="revenue_per_customer",
            color="customer_type",
            title="Revenue per Customer",
            template=CHART_TEMPLATE,
        )

        st.plotly_chart(
            fig2,
            use_container_width=True,
        )

    # ------------------------------------------------------------------------
    # Revenue / Orders / Customer Share
    # ------------------------------------------------------------------------

    share_metrics = [
        "pct_of_total_revenue",
        "pct_of_total_orders",
        "pct_of_total_customers",
    ]

    fig3 = go.Figure(
        data=[
            go.Bar(
                name=metric,
                x=customer_type_summary[
                    "customer_type"
                ],
                y=customer_type_summary[
                    metric
                ],
            )
            for metric in share_metrics
        ]
    )

    fig3.update_layout(
        barmode="group",
        title=(
            "Share of Revenue / Orders / "
            "Customers (%)"
        ),
        template=CHART_TEMPLATE,
    )

    st.plotly_chart(
        fig3,
        use_container_width=True,
    )

    # ------------------------------------------------------------------------
    # Data Table
    # ------------------------------------------------------------------------

    st.dataframe(
        customer_type_summary,
        use_container_width=True,
        hide_index=True,
    )


# ============================================================================
# SECTION: ORDER FREQUENCY BUCKETS
# ============================================================================

elif section == "Order Frequency Buckets":

    order_bucket_distribution = tables[
        "order_bucket_distribution"
    ]

    st.subheader("🧮 Order Count Buckets")

    # ------------------------------------------------------------------------
    # Customer Count by Order Frequency
    # ------------------------------------------------------------------------

    fig = px.funnel(
        order_bucket_distribution,
        x="num_customers",
        y="order_bucket",
        title="Customers by Order Frequency Bucket",
        template=CHART_TEMPLATE,
    )

    st.plotly_chart(
        fig,
        use_container_width=True,
    )

    # ------------------------------------------------------------------------
    # Revenue and Customer Share
    # ------------------------------------------------------------------------

    col1, col2 = st.columns(2)

    with col1:

        fig2 = px.pie(
            order_bucket_distribution,
            names="order_bucket",
            values="total_revenue",
            title="Revenue Share by Order Bucket",
            template=CHART_TEMPLATE,
        )

        st.plotly_chart(
            fig2,
            use_container_width=True,
        )

    with col2:

        fig3 = px.bar(
            order_bucket_distribution,
            x="order_bucket",
            y=[
                "pct_of_customers",
                "pct_of_revenue",
            ],
            barmode="group",
            title=(
                "% of Customers vs "
                "% of Revenue by Bucket"
            ),
            template=CHART_TEMPLATE,
        )

        st.plotly_chart(
            fig3,
            use_container_width=True,
        )

    # ------------------------------------------------------------------------
    # Data Table
    # ------------------------------------------------------------------------

    st.dataframe(
        order_bucket_distribution,
        use_container_width=True,
        hide_index=True,
    )