"""Dedicated Product & Category Configuration Page for Organic Foods."""

import os
import streamlit as st
import pandas as pd

from config import CURRENCY
from utils.cart_manager import go_to
from db_manager import update_product_db
from products import get_products_by_category, get_all_categories


def update_all_products(edited_df: pd.DataFrame, cat_map_by_name: dict) -> bool:
    """Save updates from st.data_editor to MySQL database & products.csv."""
    try:
        csv_path = "products.csv"
        df_csv = pd.read_csv(csv_path) if os.path.exists(csv_path) else None

        for idx, row in edited_df.iterrows():
            p_id = row.get("Product ID")
            p_name = str(row.get("Product Name", "")).strip()
            c_name = row.get("Category")
            cat_id = cat_map_by_name.get(c_name, 1)
            price = float(row.get("Price (₹)", 0.0))
            discount = float(row.get("Discount %", 0.0))
            quantity = int(row.get("Stock Qty", 50))

            if str(p_id).isdigit():
                update_product_db(int(p_id), p_name, cat_id, price, discount, quantity)

            if df_csv is not None and "product_id" in df_csv.columns:
                match_mask = df_csv["product_id"] == p_id
                if match_mask.any():
                    df_csv.loc[match_mask, "product_name"] = p_name
                    df_csv.loc[match_mask, "category_id"] = cat_id
                    df_csv.loc[match_mask, "price"] = price
                    df_csv.loc[match_mask, "discount"] = discount
                    df_csv.loc[match_mask, "quantity"] = quantity

        if df_csv is not None:
            df_csv.to_csv(csv_path, index=False)

        return True
    except Exception as e:
        print(f"Error updating product master data: {e}")
        return False


def render_product_config_page():
    """Render clean, user-friendly Product & Category Configuration Page."""
    
    # Navigation header bar with Back to Store action
    col_back, _ = st.columns([2, 8])
    with col_back:
        if st.button("← Back to Organic Store", key="prod_config_back_btn"):
            go_to("home")
            st.rerun()

    st.markdown(
        """
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
                        ⚙️ Product Configuration
                    </h1>
                    <div style="font-family:'Poppins', sans-serif; color: #86EFAC; font-size: 1.05rem; font-weight: 700;">
                        Master Catalog Editor — Filter by category, edit product names, prices, discounts, and inventory units.
                    </div>
                </div>
                <div style="text-align:right;">
                    <span style="font-size: 3rem;">📦</span>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    categories = get_all_categories()
    cat_options = ["📂 All Categories"] + [f"{c.name}" for c in categories]
    cat_map_by_name = {c.name: c.category_id for c in categories}
    cat_map_by_id = {c.category_id: c.name for c in categories}

    col_cat_sel, col_search = st.columns([1.5, 2])
    with col_cat_sel:
        selected_cat_filter = st.selectbox("📂 Category Filter", cat_options, key="clean_page_editor_cat_filter")
    with col_search:
        search_query = st.text_input("🔍 Search Products", placeholder="Search by product name...", key="clean_page_editor_prod_search")

    if selected_cat_filter == "📂 All Categories":
        prods = get_products_by_category("all")
    else:
        cat_id = cat_map_by_name.get(selected_cat_filter, 1)
        prods = get_products_by_category(str(cat_id))

    if search_query:
        q = search_query.lower().strip()
        prods = [p for p in prods if q in p.name.lower() or q in str(p.id)]

    # Quick Summary Metrics Bar
    if prods:
        avg_price = sum(p.price for p in prods) / len(prods) if prods else 0.0
        avg_disc = sum(p.discount_pct or 0 for p in prods) / len(prods) if prods else 0.0
        m1, m2, m3, m4 = st.columns(4)
        m1.metric("📦 Displayed Products", f"{len(prods)} Items")
        m2.metric("📂 Selected Category", selected_cat_filter.replace("📂 ", ""))
        m3.metric("💰 Average Selling Price", f"₹{avg_price:,.2f}")
        m4.metric("🏷️ Average Discount", f"{avg_disc:.0f}% OFF")

    st.markdown("<hr style='border:0; height:1px; background:#E2E9E3; margin: 1.2rem 0;'>", unsafe_allow_html=True)

    # Build DataFrame for st.data_editor (Keeping Product ID internally for DB updates)
    editor_data = []
    for p in prods:
        c_name = cat_map_by_id.get(p.category_id, f"Category {p.category_id}")
        editor_data.append({
            "Product ID": int(p.id) if str(p.id).isdigit() else p.id,
            "Product Name": p.name,
            "Category": c_name,
            "Price (₹)": float(p.price),
            "Discount %": float(p.discount_pct or 0),
            "Stock Qty": int(getattr(p, "quantity", 50)),
            "Unit": p.unit or "kg"
        })

    df_editor = pd.DataFrame(editor_data)

    st.markdown("##### ✏️ Product Catalog Table")
    st.caption("Double-click any product cell below to edit name, category, price, discount, or stock quantity.")

    edited_df = st.data_editor(
        df_editor,
        column_order=["Product Name", "Category", "Price (₹)", "Discount %", "Stock Qty", "Unit"],
        column_config={
            "Product Name": st.column_config.TextColumn(
                "Product Name", help="Edit product name", required=True, width="large"
            ),
            "Category": st.column_config.SelectboxColumn(
                "Category",
                help="Select product category",
                options=list(cat_map_by_name.keys()),
                required=True,
                width="medium"
            ),
            "Price (₹)": st.column_config.NumberColumn(
                "Price (₹)", min_value=0.0, step=1.0, format="₹%.2f", required=True, width="medium"
            ),
            "Discount %": st.column_config.NumberColumn(
                "Discount %", min_value=0.0, max_value=100.0, step=1.0, format="%d%%", width="medium"
            ),
            "Stock Qty": st.column_config.NumberColumn(
                "Stock Qty", min_value=0, step=1, format="%d", width="medium"
            ),
            "Unit": st.column_config.SelectboxColumn(
                "Unit", options=["kg", "g", "L", "mL", "pack"], required=True, width="small"
            )
        },
        use_container_width=True,
        hide_index=True,
        num_rows="dynamic",
        key="clean_prod_config_grid"
    )

    st.markdown("<div style='margin-bottom:1.5rem;'></div>", unsafe_allow_html=True)
    col_save, col_spacer = st.columns([2.5, 3.5])
    with col_save:
        if st.button("💾 Save All Changes", type="primary", use_container_width=True, key="btn_save_clean_prod_config"):
            save_ok = update_all_products(edited_df, cat_map_by_name)
            if save_ok:
                st.cache_data.clear()
                st.success("🎉 All product and category updates saved successfully to Database & CSV!")
                st.rerun()
            else:
                st.error("Error saving product changes. Please check log.")
