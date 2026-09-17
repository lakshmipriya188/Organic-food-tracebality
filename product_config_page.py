"""Product Configurations Page Component for Organic Food Traceability.

Provides a dedicated, systematic category-wise product editor for live database updates
(product name, base price, discount %, unit measure, and stock quantity).
"""

import streamlit as st
import pandas as pd
from config import CURRENCY, APP_NAME
from utils.cart_manager import go_to
from db_manager import (
    fetch_all_products_db,
    fetch_all_categories_db,
    update_product_db
)


def render_product_config_page():
    """Render standalone Product Configurations Management page."""

    # Top Navigation Back Button
    col_back, _ = st.columns([2, 8])
    with col_back:
        if st.button("← Back to Organic Store", key="pconfig_back_btn"):
            go_to("home")
            st.rerun()

    st.markdown("<div style='margin-bottom: 0.8rem;'></div>", unsafe_allow_html=True)

    # 1. HEADER BANNER
    st.markdown(
        f"""
        <div style="
            background: linear-gradient(135deg, #0F291E 0%, #1B4D3E 50%, #16A34A 100%);
            border-radius: 20px;
            padding: 2rem 2.2rem;
            color: #FFFFFF;
            box-shadow: 0 15px 35px rgba(27, 77, 62, 0.22);
            border: 1px solid rgba(134, 239, 172, 0.3);
            margin-bottom: 1.8rem;
        ">
            <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:1.2rem;">
                <div>
                    <h1 style="font-family:'Poppins', sans-serif; color: #FFFFFF !important; margin: 0 0 0.4rem 0; font-size: 2.2rem; font-weight: 800; letter-spacing: -0.5px;">
                        ⚙️ Product Configurations
                    </h1>
                    <div style="font-family:'Poppins', sans-serif; color: #86EFAC; font-size: 1.05rem; font-weight: 600;">
                        Category-wise Live Database Product, Pricing & Discount Management
                    </div>
                </div>
                <div style="text-align:right;">
                    <span style="font-size: 3rem;">🛠️</span>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    # 2. FETCH REAL-TIME DATA FROM DATABASE
    db_products = fetch_all_products_db()
    db_cats = fetch_all_categories_db()

    if not db_cats:
        db_cats = [
            {"category_id": 1, "category_name": "Fruits"},
            {"category_id": 2, "category_name": "Vegetables"},
            {"category_id": 3, "category_name": "Grains"},
            {"category_id": 4, "category_name": "Pulses"},
            {"category_id": 5, "category_name": "Dairy"},
            {"category_id": 6, "category_name": "Spices"},
            {"category_id": 7, "category_name": "Beverages"},
            {"category_id": 8, "category_name": "Dry Fruits"},
            {"category_id": 9, "category_name": "Millets"},
            {"category_id": 10, "category_name": "Oils"},
        ]

    # Metrics Summary Cards
    total_prods = len(db_products)
    total_categories = len(db_cats)
    discounted_prods = sum(1 for p in db_products if float(p.get("discount") or 0.0) > 0)
    total_stock_units = sum(int(p.get("quantity") or 0) for p in db_products)

    m1, m2, m3, m4 = st.columns(4)
    with m1:
        st.metric(label="📦 Total Live Products", value=f"{total_prods}", delta="Database Synced")
    with m2:
        st.metric(label="📂 Product Categories", value=f"{total_categories}", delta="Catalog Groups")
    with m3:
        st.metric(label="🔥 Active Discount Items", value=f"{discounted_prods}", delta="Special Offers")
    with m4:
        st.metric(label="📊 Total Inventory Stock", value=f"{total_stock_units:,} Units", delta="Live Units")

    st.markdown("<hr style='border:0; height:1px; background:#E2E9E3; margin: 1.5rem 0 1.5rem 0;'>", unsafe_allow_html=True)

    # Quick Search Filter across catalog
    search_q = st.text_input("🔍 Search Products across Categories", placeholder="Type product name, category or product ID...")
    st.markdown("<div style='margin-bottom: 1rem;'></div>", unsafe_allow_html=True)

    # 3. CATEGORY-WISE PRODUCT CONFIGURATION TABS
    cat_names = [c["category_name"] for c in db_cats]
    cat_tabs = st.tabs([f"📂 {name}" for name in cat_names])

    for idx, cat in enumerate(db_cats):
        c_id = cat["category_id"]
        c_name = cat["category_name"]

        with cat_tabs[idx]:
            cat_prods = [p for p in db_products if p.get("category_id") == c_id]
            
            if search_q:
                sq = search_q.lower()
                cat_prods = [p for p in cat_prods if sq in str(p.get("product_name", "")).lower() or sq in str(p.get("product_id", ""))]

            if not cat_prods:
                st.info(f"No matching products found in category '{c_name}'.")
                continue

            st.markdown(
                f"""
                <div style="font-family:'Poppins', sans-serif; font-size:1.2rem; font-weight:700; color:#1B4D3E; margin-bottom: 0.8rem;">
                    Configuring {len(cat_prods)} Product(s) in <span style="color:#16A34A;">{c_name}</span>
                </div>
                """,
                unsafe_allow_html=True
            )

            for p in cat_prods:
                p_id = p["product_id"]
                curr_name = str(p.get("product_name") or "")
                curr_price = float(p.get("price") or 0.0)
                curr_disc = float(p.get("discount") or 0.0)
                curr_unit = str(p.get("unit") or "kg")
                curr_qty = int(p.get("quantity") or 50)
                final_p = round(curr_price * (1 - (curr_disc / 100.0)), 2)

                expander_label = f"📦 Product #{p_id}: {curr_name} — Base MRP: {CURRENCY}{curr_price:,.2f} | Discount: {curr_disc:.0f}% OFF | Final Price: {CURRENCY}{final_p:,.2f}/{curr_unit}"
                
                with st.expander(expander_label, expanded=False):
                    with st.form(key=f"pcfg_form_{p_id}"):
                        ec1, ec2, ec3 = st.columns([2.5, 1.2, 1.2])
                        with ec1:
                            new_name = st.text_input("Product Name", value=curr_name, key=f"pcfg_name_{p_id}")
                        with ec2:
                            new_price = st.number_input(
                                "Base Price / MRP (₹)",
                                value=curr_price,
                                min_value=0.0,
                                step=5.0,
                                key=f"pcfg_price_{p_id}"
                            )
                        with ec3:
                            new_disc = st.number_input(
                                "Discount (%)",
                                value=curr_disc,
                                min_value=0.0,
                                max_value=100.0,
                                step=1.0,
                                key=f"pcfg_disc_{p_id}"
                            )

                        ec4, ec5, ec6 = st.columns([1.5, 1.5, 2])
                        with ec4:
                            unit_options = ["kg", "L", "g", "pack"]
                            unit_idx = unit_options.index(curr_unit) if curr_unit in unit_options else 0
                            new_unit = st.selectbox(
                                "Unit Measure",
                                options=unit_options,
                                index=unit_idx,
                                key=f"pcfg_unit_{p_id}"
                            )
                        with ec5:
                            new_qty = st.number_input(
                                "Stock Quantity",
                                value=curr_qty,
                                min_value=0,
                                step=5,
                                key=f"pcfg_qty_{p_id}"
                            )
                        with ec6:
                            calc_final = round(new_price * (1 - (new_disc / 100.0)), 2)
                            st.markdown(
                                f"""
                                <div style="background:#F0FDF4; border:1px solid #BBF7D0; border-radius:10px; padding:0.6rem; margin-top:1.5rem; text-align:center;">
                                    <span style="font-size:0.75rem; color:#166534; font-weight:700;">FINAL SELLING PRICE</span><br>
                                    <span style="font-size:1.15rem; color:#16A34A; font-weight:800; font-family:'Poppins', sans-serif;">{CURRENCY}{calc_final:,.2f} / {new_unit}</span>
                                </div>
                                """,
                                unsafe_allow_html=True
                            )

                        save_submitted = st.form_submit_button(
                            "💾 Save Product Changes",
                            type="primary",
                            use_container_width=True
                        )
                        if save_submitted:
                            ok, msg = update_product_db(p_id, new_name, new_price, new_disc, new_unit, new_qty)
                            if ok:
                                st.cache_data.clear()
                                st.success(msg)
                                st.rerun()
                            else:
                                st.error(msg)
