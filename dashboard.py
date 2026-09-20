"""Central Analytics & Admin Dashboard for Organic Food Traceability.

Integrates complete Sales Analytics (Plotly/Altair charts, RFM segmentation,
customer performance, product analysis, discount buckets, monthly trends)
from precomputed analytics with real-time MySQL database operations.
"""

import os
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import altair as alt

from config import CURRENCY, APP_NAME
from db_manager import fetch_all_customers_db, fetch_all_orders_db, fetch_bestsellers_db, fetch_deals_db
from products import get_products_by_category, get_all_categories, find_product_icon


PRECOMPUTED_DIR = "precomputed"
CHART_TEMPLATE = "plotly_white"

FILES = {
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
    "customer_summary": "customer_summary.csv",
    "top_customers": "top_10_customers.csv",
    "inactive_days_summary": "inactive_days_summary.csv",
    "active_days_summary": "active_days_summary.csv",
}


@st.cache_data
def load_precomputed(path):
    """Load a precomputed CSV file safely."""
    if os.path.exists(path):
        return pd.read_csv(path)
    return None


def get_all_tables():
    """Load precomputed CSV summary tables."""
    tables = {}
    if not os.path.isdir(PRECOMPUTED_DIR):
        return tables

    for name, filename in FILES.items():
        filepath = os.path.join(PRECOMPUTED_DIR, filename)
        tables[name] = load_precomputed(filepath)

    if "discount_bucket_summary" in tables and tables["discount_bucket_summary"] is not None:
        discount_order = ["0%", "1-5%", "6-10%", "11-20%", "21-30%", "30%+"]
        tables["discount_bucket_summary"]["discount_group"] = pd.Categorical(
            tables["discount_bucket_summary"]["discount_group"],
            categories=discount_order,
            ordered=True
        )
        tables["discount_bucket_summary"] = tables["discount_bucket_summary"].sort_values("discount_group")

    if "order_bucket_distribution" in tables and tables["order_bucket_distribution"] is not None:
        order_bucket_order = ["1 (one-time)", "2", "3-5", "6-10", "10+"]
        tables["order_bucket_distribution"]["order_bucket"] = pd.Categorical(
            tables["order_bucket_distribution"]["order_bucket"],
            categories=order_bucket_order,
            ordered=True
        )
        tables["order_bucket_distribution"] = tables["order_bucket_distribution"].sort_values("order_bucket")

    if "dow_revenue" in tables and tables["dow_revenue"] is not None:
        dow_order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        tables["dow_revenue"]["day_of_week"] = pd.Categorical(
            tables["dow_revenue"]["day_of_week"],
            categories=dow_order,
            ordered=True
        )
        tables["dow_revenue"] = tables["dow_revenue"].sort_values("day_of_week")

    if "inactive_days_summary" in tables and tables["inactive_days_summary"] is not None:
        inactive_order = ["0 days", "1-3 days", "4-7 days", "8-30 days", "31-90 days", "90+ days"]
        tables["inactive_days_summary"]["inactive_days_group"] = pd.Categorical(
            tables["inactive_days_summary"]["inactive_days_group"],
            categories=inactive_order,
            ordered=True
        )
        tables["inactive_days_summary"] = tables["inactive_days_summary"].sort_values("inactive_days_group")

    if "active_days_summary" in tables and tables["active_days_summary"] is not None:
        active_order = ["1-3 days", "4-7 days", "8-30 days"]
        tables["active_days_summary"]["active_days_group"] = pd.Categorical(
            tables["active_days_summary"]["active_days_group"],
            categories=active_order,
            ordered=True
        )
        tables["active_days_summary"] = tables["active_days_summary"].sort_values("active_days_group")

    return tables


def kpi_row(items):
    """Display multiple KPI metrics in a single row."""
    columns = st.columns(len(items))
    for column, (label, value) in zip(columns, items):
        column.metric(label, value)


def render_dashboard():
    """Render the central Admin & Sales Analytics Dashboard."""

    admin_user = st.session_state.get("user", "Admin")

    st.markdown(
        f"""
        <div style="
            background: linear-gradient(135deg, #0F291E 0%, #1B4D3E 50%, #16A34A 100%);
            border-radius: 20px;
            padding: 1.8rem 2.2rem;
            color: #FFFFFF;
            box-shadow: 0 15px 35px rgba(27, 77, 62, 0.22);
            border: 1px solid rgba(134, 239, 172, 0.3);
            margin-bottom: 1.5rem;
        ">
            <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:1.2rem;">
                <div>
                    <h1 style="font-family:'Poppins', sans-serif; color: #FFFFFF !important; margin: 0 0 0.3rem 0; font-size: 2.2rem; font-weight: 800; letter-spacing: -0.5px;">
                        Sales Analytics & Business Intelligence Dashboard
                    </h1>
                    <div style="font-family:'Poppins', sans-serif; color: #86EFAC; font-size: 1.05rem; font-weight: 700;">
                        Welcome back, {admin_user}! 😊
                    </div>
                </div>
                <div style="text-align:right;">
                    <span style="font-size: 3rem;">📊</span>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    tables = get_all_tables()

    sections = [
        "📊 Overview",
        "👥 Customer Performance",
        "🏆 Product Performance",
        "📅 Day-of-Week Trends",
        "📈 Monthly Revenue Trend",
        "🏷️ Discount Analysis",
        "🎯 RFM Segmentation",
        "🔁 New vs Returning Customers",
        "🧮 Order Frequency Buckets",
        "⚙️ Live Admin Operations"
    ]

    if "dash_active_section" not in st.session_state:
        st.session_state.dash_active_section = "📊 Overview"

    selected_section = st.selectbox(
        "Select Dashboard Section",
        sections,
        index=sections.index(st.session_state.dash_active_section) if st.session_state.dash_active_section in sections else 0,
        key="dash_section_select"
    )
    st.session_state.dash_active_section = selected_section

    st.markdown("<hr style='border:0; height:1px; background:#E2E9E3; margin: 1.2rem 0;'>", unsafe_allow_html=True)

    if selected_section == "📊 Overview":
        st.subheader("📊 Executive Overview")

        if "kpis" in tables and tables["kpis"] is not None and not tables["kpis"].empty:
            kpi = tables["kpis"].iloc[0]
            kpi_row([
                ("Total Revenue", f"₹{kpi['total_revenue']:,.0f}"),
                ("Total Orders", f"{int(kpi['total_orders']):,}"),
                ("Unique Customers", f"{int(kpi['unique_customers']):,}"),
                ("Unique Products", f"{int(kpi['unique_products']):,}"),
                ("Avg Order Value", f"₹{kpi['avg_order_value']:,.2f}"),
            ])
            st.divider()

        col1, col2 = st.columns(2)

        with col1:
            if "monthly_revenue" in tables and tables["monthly_revenue"] is not None:
                fig = px.line(
                    tables["monthly_revenue"],
                    x="month",
                    y="total_revenue",
                    markers=True,
                    title="Monthly Revenue Trend",
                    template=CHART_TEMPLATE,
                )
                fig.update_layout(xaxis_title="Month", yaxis_title="Revenue (₹)")
                st.plotly_chart(fig, use_container_width=True)

        with col2:
            if "customer_type_summary" in tables and tables["customer_type_summary"] is not None:
                fig = px.pie(
                    tables["customer_type_summary"],
                    names="customer_type",
                    values="total_revenue",
                    title="Revenue Split: New vs Returning Customers",
                    hole=0.45,
                    template=CHART_TEMPLATE,
                )
                st.plotly_chart(fig, use_container_width=True)

    elif selected_section == "👥 Customer Performance":
        st.subheader("👥 Customer Performance Overview")

        if "customer_summary" in tables and tables["customer_summary"] is not None:
            c_df = tables["customer_summary"]
            tot_cust = c_df["customer_id"].nunique()
            act_cust = c_df["status"].eq("Active").sum()
            inact_cust = c_df["status"].eq("Inactive").sum()
            tot_rev = c_df["total_revenue"].sum()
            avg_val = c_df["total_revenue"].mean()
            avg_aov = c_df["avg_order_value"].mean()
            tot_ord = c_df["total_orders"].sum()

            c1, c2, c3, c4 = st.columns(4)
            c1.metric("Total Customers", f"{tot_cust:,}")
            c2.metric("Active Customers", f"{act_cust:,}")
            c3.metric("Inactive Customers", f"{inact_cust:,}")
            c4.metric("Total Revenue", f"₹{tot_rev:,.0f}")

            c5, c6, c7 = st.columns(3)
            c5.metric("Avg Customer Value", f"₹{avg_val:,.0f}")
            c6.metric("Avg Order Value", f"₹{avg_aov:,.0f}")
            c7.metric("Total Orders", f"{tot_ord:,}")

            st.divider()

        if "top_customers" in tables and tables["top_customers"] is not None:
            st.subheader("🏆 Top 10 High-Value Customers")
            st.dataframe(tables["top_customers"], use_container_width=True, hide_index=True)
            st.divider()

        if "inactive_days_summary" in tables and tables["inactive_days_summary"] is not None:
            st.subheader("📉 Inactive Days Distribution")
            inactive_chart = (
                alt.Chart(tables["inactive_days_summary"])
                .mark_bar()
                .encode(
                    x=alt.X("inactive_days_group:N", sort=["0 days", "1-3 days", "4-7 days", "8-30 days", "31-90 days", "90+ days"], title="Inactive Days Group"),
                    y=alt.Y("customer_count:Q", title="Customers"),
                    tooltip=["inactive_days_group:N", "customer_count:Q", "customer_pct:Q", "total_revenue:Q"]
                )
                .properties(height=350)
            )
            st.altair_chart(inactive_chart, use_container_width=True)

    elif selected_section == "🏆 Product Performance":
        st.subheader("🏆 Product Revenue & Sales Performance")

        top_10 = tables.get("top_10_products")
        prod_sum = tables.get("product_summary")

        if top_10 is not None and prod_sum is not None:
            col1, col2 = st.columns(2)
            with col1:
                fig2 = px.treemap(
                    top_10,
                    path=["product_id"],
                    values="total_revenue",
                    color="avg_discount",
                    color_continuous_scale="RdYlGn_r",
                    title="Revenue Share of Top 10 Products (size = revenue, color = avg discount)",
                    template=CHART_TEMPLATE,
                )
                st.plotly_chart(fig2, use_container_width=True)

            with col2:
                fig3 = px.scatter(
                    prod_sum,
                    x="avg_price",
                    y="total_quantity",
                    size="total_revenue",
                    color="revenue_share_pct",
                    hover_name="product_id",
                    title="Price vs Quantity Sold (bubble = revenue)",
                    template=CHART_TEMPLATE,
                    color_continuous_scale="Viridis",
                )
                st.plotly_chart(fig3, use_container_width=True)

            st.markdown("##### 📦 Top 10 Products Breakdown")
            st.dataframe(top_10, use_container_width=True, hide_index=True)

    elif selected_section == "📅 Day-of-Week Trends":
        st.subheader("📅 Sales Revenue by Day of Week")

        dow_revenue = tables.get("dow_revenue")
        if dow_revenue is not None:
            fig = px.line_polar(
                dow_revenue,
                r="total_revenue",
                theta="day_of_week",
                line_close=True,
                title="Revenue Radar by Day of Week",
                template=CHART_TEMPLATE,
            )
            fig.update_traces(fill="toself")
            st.plotly_chart(fig, use_container_width=True)

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
                st.plotly_chart(fig2, use_container_width=True)

            with col2:
                fig3 = px.funnel(
                    dow_revenue.sort_values("total_revenue", ascending=False),
                    x="total_revenue",
                    y="day_of_week",
                    title="Days Ranked by Total Revenue",
                    template=CHART_TEMPLATE,
                )
                st.plotly_chart(fig3, use_container_width=True)

            st.dataframe(dow_revenue, use_container_width=True, hide_index=True)

    elif selected_section == "📈 Monthly Revenue Trend":
        st.subheader("📈 Monthly Revenue & Cumulative Growth")

        monthly_rev = tables.get("monthly_revenue")
        if monthly_rev is not None:
            fig = go.Figure()
            fig.add_trace(go.Bar(x=monthly_rev["month"], y=monthly_rev["total_revenue"], name="Monthly Revenue"))
            fig.add_trace(go.Scatter(x=monthly_rev["month"], y=monthly_rev["cumulative_revenue"], name="Cumulative Revenue", yaxis="y2", mode="lines+markers"))
            fig.update_layout(
                title="Monthly Revenue with Cumulative Overlay",
                yaxis=dict(title="Monthly Revenue (₹)"),
                yaxis2=dict(title="Cumulative Revenue (₹)", overlaying="y", side="right"),
                template=CHART_TEMPLATE,
            )
            st.plotly_chart(fig, use_container_width=True)

            col1, col2 = st.columns(2)
            with col1:
                fig2 = px.bar(
                    monthly_rev,
                    x="month",
                    y="mom_growth_pct",
                    color="mom_growth_pct",
                    color_continuous_scale="RdYlGn",
                    title="Month-over-Month Growth %",
                    template=CHART_TEMPLATE,
                )
                st.plotly_chart(fig2, use_container_width=True)

            with col2:
                fig3 = px.area(
                    monthly_rev,
                    x="month",
                    y="pct_of_total",
                    title="Share of Total Revenue by Month",
                    template=CHART_TEMPLATE,
                )
                st.plotly_chart(fig3, use_container_width=True)

            st.dataframe(monthly_rev, use_container_width=True, hide_index=True)

    elif selected_section == "🏷️ Discount Analysis":
        st.subheader("🏷️ Discount Bucket & Margin Impact Analysis")

        disc_df = tables.get("discount_bucket_summary")
        if disc_df is not None:
            fig = px.bar(
                disc_df,
                x="discount_group",
                y="total_revenue",
                color="revenue_share_pct",
                color_continuous_scale="Sunset",
                title="Revenue by Discount Bucket",
                template=CHART_TEMPLATE,
            )
            st.plotly_chart(fig, use_container_width=True)

            col1, col2 = st.columns(2)
            with col1:
                fig2 = px.pie(
                    disc_df,
                    names="discount_group",
                    values="total_qty",
                    title="Quantity Sold Share by Discount Bucket",
                    template=CHART_TEMPLATE,
                )
                st.plotly_chart(fig2, use_container_width=True)

            with col2:
                fig3 = px.scatter(
                    disc_df,
                    x="avg_qty",
                    y="unique_customers",
                    size="total_revenue",
                    color="discount_group",
                    title="Avg Qty vs Unique Customers by Discount Bucket",
                    template=CHART_TEMPLATE,
                )
                st.plotly_chart(fig3, use_container_width=True)

            st.dataframe(disc_df, use_container_width=True, hide_index=True)

    elif selected_section == "🎯 RFM Segmentation":
        st.subheader("🎯 RFM (Recency, Frequency, Monetary) Customer Segmentation")

        rfm = tables.get("rfm")
        seg_sum = tables.get("segment_summary")

        if seg_sum is not None:
            fig = px.treemap(
                seg_sum,
                path=["segment"],
                values="customer_count",
                color="total_revenue",
                color_continuous_scale="Blues",
                title="Customer Segments (size = customer count, color = revenue)",
                template=CHART_TEMPLATE,
            )
            st.plotly_chart(fig, use_container_width=True)

            col1, col2 = st.columns(2)
            with col1:
                fig2 = px.bar(
                    seg_sum.sort_values("total_revenue"),
                    x="total_revenue",
                    y="segment",
                    orientation="h",
                    title="Total Revenue by RFM Segment",
                    template=CHART_TEMPLATE,
                )
                st.plotly_chart(fig2, use_container_width=True)

            with col2:
                if rfm is not None:
                    fig3 = px.scatter_3d(
                        rfm,
                        x="R_score",
                        y="F_score",
                        z="M_score",
                        color="segment",
                        opacity=0.7,
                        title="3D RFM Score Cube",
                        template=CHART_TEMPLATE,
                    )
                    st.plotly_chart(fig3, use_container_width=True)

            st.dataframe(seg_sum, use_container_width=True, hide_index=True)

    elif selected_section == "🔁 New vs Returning Customers":
        st.subheader("🔁 New vs Returning Customer Analysis")

        cust_type = tables.get("customer_type_summary")
        if cust_type is not None:
            col1, col2 = st.columns(2)
            with col1:
                fig = px.pie(
                    cust_type,
                    names="customer_type",
                    values="unique_customers",
                    title="Customer Count Split",
                    hole=0.4,
                    template=CHART_TEMPLATE,
                )
                st.plotly_chart(fig, use_container_width=True)

            with col2:
                fig2 = px.bar(
                    cust_type,
                    x="customer_type",
                    y="revenue_per_customer",
                    color="customer_type",
                    title="Revenue per Customer (₹)",
                    template=CHART_TEMPLATE,
                )
                st.plotly_chart(fig2, use_container_width=True)

            share_metrics = ["pct_of_total_revenue", "pct_of_total_orders", "pct_of_total_customers"]
            fig3 = go.Figure(
                data=[
                    go.Bar(
                        name=metric.replace("pct_of_total_", "").capitalize(),
                        x=cust_type["customer_type"],
                        y=cust_type[metric],
                    )
                    for metric in share_metrics
                ]
            )
            fig3.update_layout(barmode="group", title="Share of Revenue / Orders / Customers (%)", template=CHART_TEMPLATE)
            st.plotly_chart(fig3, use_container_width=True)

            st.dataframe(cust_type, use_container_width=True, hide_index=True)

    elif selected_section == "🧮 Order Frequency Buckets":
        st.subheader("🧮 Order Count Frequency Distribution")

        ord_bucket = tables.get("order_bucket_distribution")
        if ord_bucket is not None:
            fig = px.funnel(
                ord_bucket,
                x="num_customers",
                y="order_bucket",
                title="Customers by Order Frequency Bucket",
                template=CHART_TEMPLATE,
            )
            st.plotly_chart(fig, use_container_width=True)

            col1, col2 = st.columns(2)
            with col1:
                fig2 = px.pie(
                    ord_bucket,
                    names="order_bucket",
                    values="total_revenue",
                    title="Revenue Share by Order Bucket",
                    template=CHART_TEMPLATE,
                )
                st.plotly_chart(fig2, use_container_width=True)

            with col2:
                fig3 = px.bar(
                    ord_bucket,
                    x="order_bucket",
                    y=["pct_of_customers", "pct_of_revenue"],
                    barmode="group",
                    title="% of Customers vs % of Revenue",
                    template=CHART_TEMPLATE,
                )
                st.plotly_chart(fig3, use_container_width=True)

            st.dataframe(ord_bucket, use_container_width=True, hide_index=True)

    elif selected_section == "⚙️ Live Admin Operations":
        st.subheader("⚙️ Live Database Operations & Catalog Directory")

        products = get_products_by_category("all")
        categories = get_all_categories()
        customers = fetch_all_customers_db()
        all_orders = fetch_all_orders_db()

        total_revenue = sum(o.get("product_count", 1) * float(o.get("price_after_discount") or o.get("product_price") or 0.0) for o in all_orders)

        c1, c2, c3, c4, c5 = st.columns(5)
        c1.metric("🛍️ Catalog Products", len(products))
        c2.metric("📂 Categories", len(categories))
        c3.metric("👥 DB Customers", len(customers))
        c4.metric("📜 DB Orders", len(all_orders))
        c5.metric("💰 Live Revenue", f"{CURRENCY}{total_revenue:,.2f}")

        st.divider()

        op_tab1, op_tab2, op_tab3 = st.tabs(["📦 Products Catalog", "👥 Customer Directory", "📜 Order Log"])

        with op_tab1:
            prod_rows = []
            for p in products:
                prod_rows.append({
                    "ID": f"#{p.id}",
                    "Product": p.name,
                    "Price": f"{CURRENCY}{p.price:,.2f}/{p.unit}",
                    "Stock": f"{getattr(p, 'quantity', 50)} {p.unit}",
                    "Origin": getattr(p, "farmer_name", "Co-Op Farmer"),
                })
            st.dataframe(pd.DataFrame(prod_rows), use_container_width=True, hide_index=True)

        with op_tab2:
            if customers:
                c_rows = [{"ID": f"#{c.get('customer_id')}", "Name": c.get('customer_name'), "Email": c.get('email_id')} for c in customers]
                st.dataframe(pd.DataFrame(c_rows), use_container_width=True, hide_index=True)
            else:
                st.info("No customer records found.")

        with op_tab3:
            if all_orders:
                o_rows = []
                for o in all_orders:
                    qty = o.get("product_count", 1)
                    p_price = float(o.get("price_after_discount") or o.get("product_price") or 0.0)
                    o_rows.append({
                        "Order ID": f"#{o.get('order_id')}",
                        "Customer": o.get("customer_name") or f"Customer #{o.get('customer_id')}",
                        "Product": o.get("product_name") or f"Product #{o.get('product_id')}",
                        "Quantity": qty,
                        "Total Amount": f"{CURRENCY}{round(qty * p_price, 2):,.2f}",
                        "Status": "COMPLETED"
                    })
                st.dataframe(pd.DataFrame(o_rows), use_container_width=True, hide_index=True)
            else:
                st.info("No orders placed yet.")