"""Product Configurations Page Component for Admin Users."""

import streamlit as st
import pandas as pd
from config import CURRENCY
from utils.cart_manager import go_to
from db_manager import fetch_all_categories_db, fetch_all_products_db, update_product_db
from products import get_all_categories, get_products_by_category


def render_product_config_page():
    """Render Admin Product Configurations Page."""

    # 1. ACCESS CONTROL: Visible ONLY to Admin users
    is_admin = bool(st.session_state.get("is_admin", False))
    if not is_admin:
        st.error("⛔ Access Denied: Product Configurations is restricted to Admin users only.")
        if st.button("← Go to Home"):
            go_to("home")
            st.rerun()
        return

    # Top Action Bar: Back to Admin Dashboard
    col_back, _ = st.columns([2.5, 7.5])
    with col_back:
        if st.button("← Back to Admin Dashboard", key="pcfg_back_btn"):
            go_to("admin")
            st.rerun()

    # Page Header Banner
    st.markdown(
        """
        <div style="
            background: linear-gradient(135deg, #0F291E 0%, #1B4D3E 50%, #16A34A 100%);
            border-radius: 20px;
            padding: 2rem 2.2rem;
            color: #FFFFFF;
            box-shadow: 0 15px 35px rgba(27, 77, 62, 0.22);
            border: 1px solid rgba(134, 239, 172, 0.3);
            margin: 1rem 0 2rem 0;
        ">
            <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:1rem;">
                <div>
                    <h1 style="font-family:'Poppins', sans-serif; color: #FFFFFF !important; margin: 0 0 0.4rem 0; font-size: 2.2rem; font-weight: 800;">
                        ⚙️ Product Configurations
                    </h1>
                    <div style="font-family:'Poppins', sans-serif; color: #86EFAC; font-size: 1.05rem; font-weight: 600;">
                        Manage, edit, and update product catalog prices, discounts, and inventory dynamically in MySQL.
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

    # 2. FETCH DATA DYNAMICALLY FROM MYSQL DATABASE
    db_categories = fetch_all_categories_db()
    db_products = fetch_all_products_db()

    # Fallback if DB empty or unavailable
    if not db_categories:
        fallback_cats = get_all_categories()
        db_categories = [{"category_id": c.category_id, "category_name": c.name} for c in fallback_cats]

    if not db_products:
        fallback_prods = get_products_by_category("all")
        db_products = []
        for p in fallback_prods:
            mrp = p.original_price or p.price
            disc = p.discount_pct or 0
            db_products.append({
                "product_id": int(p.id) if str(p.id).isdigit() else p.id,
                "category_id": p.category_id,
                "product_name": p.name,
                "price": float(mrp),
                "discount": float(disc),
                "unit": p.unit,
                "quantity": getattr(p, "quantity", 50),
                "manufacture_date": getattr(p, "manufacture_date", "2026-07-20"),
                "expiry_date": getattr(p, "expiry_date", "2026-08-05"),
                "category_name": p.category_slug.capitalize()
            })

    # Category Mapping
    cat_id_to_name = {c["category_id"]: c["category_name"] for c in db_categories}

    # 3. EDIT PRODUCT FORM / MODAL CONTAINER
    editing_prod = st.session_state.get("editing_product")

    if editing_prod:
        st.markdown(
            """
            <div style="
                background: #FFFFFF;
                border: 2px solid #22C55E;
                border-radius: 20px;
                padding: 1.8rem;
                margin-bottom: 2rem;
                box-shadow: 0 10px 30px rgba(34, 197, 94, 0.15);
            ">
            <h3 style="font-family:'Poppins', sans-serif; color: #1B4D3E; margin-top: 0; margin-bottom: 0.5rem;">
                ✏️ Edit Product Details
            </h3>
            """,
            unsafe_allow_html=True
        )

        p_id = editing_prod.get("product_id")
        cur_name = editing_prod.get("product_name", "")
        cur_cat_id = editing_prod.get("category_id", 1)
        cur_cat_name = cat_id_to_name.get(cur_cat_id, editing_prod.get("category_name", "Category"))
        cur_price = float(editing_prod.get("price") or 0.0)
        cur_disc = float(editing_prod.get("discount") or 0.0)
        cur_qty = int(editing_prod.get("quantity") or 50)
        cur_unit = editing_prod.get("unit") or "kg"
        cur_mfg = str(editing_prod.get("manufacture_date") or "2026-07-20")
        cur_exp = str(editing_prod.get("expiry_date") or "2026-08-05")

        with st.form("edit_product_form"):
            col_e1, col_e2 = st.columns(2)
            with col_e1:
                st.text_input("Product ID (Unique Database ID)", value=f"#{p_id}", disabled=True)
                new_name = st.text_input("Product Name", value=cur_name, placeholder="Enter product name")
                st.text_input("Category", value=cur_cat_name, disabled=True)
                new_unit = st.selectbox("Unit Measure", options=["kg", "L", "g"], index=["kg", "L", "g"].index(cur_unit) if cur_unit in ["kg", "L", "g"] else 0)

            with col_e2:
                new_price = st.number_input("MRP Price (₹)", value=cur_price, min_value=0.01, step=5.0, format="%.2f")
                new_disc = st.number_input("Discount Percentage (%)", value=cur_disc, min_value=0.0, max_value=100.0, step=1.0, format="%.2f")
                new_qty = st.number_input("Stock Quantity", value=cur_qty, min_value=0, step=1)
                new_mfg = st.text_input("Manufacturing Date", value=cur_mfg)

            new_exp = st.text_input("Expiry Date", value=cur_exp)

            # Real-time Discount Calculation Preview
            calc_final_price = round(new_price - (new_price * (new_disc / 100.0)), 2)
            st.markdown(
                f"""
                <div style="
                    background: #DCFCE7;
                    border: 1px solid #86EFAC;
                    border-radius: 12px;
                    padding: 10px 16px;
                    margin: 1rem 0;
                    display: flex;
                    justify-content: space-between;
                    align-items: center;
                ">
                    <span style="font-weight: 700; color: #166534;">
                        📊 Calculated Final Price (After {new_disc:.0f}% Discount):
                    </span>
                    <span style="font-family: 'Poppins', sans-serif; font-size: 1.4rem; font-weight: 800; color: #16A34A;">
                        {CURRENCY}{calc_final_price:,.2f} / {new_unit}
                    </span>
                </div>
                """,
                unsafe_allow_html=True
            )

            btn_col_save, btn_col_cancel = st.columns([1, 1])
            with btn_col_save:
                submitted_save = st.form_submit_button("💾 Save Changes", type="primary", use_container_width=True)
            with btn_col_cancel:
                submitted_cancel = st.form_submit_button("❌ Cancel", use_container_width=True)

            if submitted_save:
                # Validation checks
                if not new_name.strip():
                    st.error("⚠️ Product Name cannot be empty.")
                elif new_price <= 0:
                    st.error("⚠️ Price must be greater than zero.")
                elif new_disc < 0 or new_disc > 100:
                    st.error("⚠️ Discount percentage must be between 0% and 100%.")
                else:
                    success, msg = update_product_db(
                        product_id=p_id,
                        product_name=new_name.strip(),
                        price=new_price,
                        discount=new_disc,
                        quantity=new_qty,
                        unit=new_unit,
                        manufacture_date=new_mfg.strip(),
                        expiry_date=new_exp.strip()
                    )
                    if success:
                        st.session_state.editing_product = None
                        st.success(f"✅ Product #{p_id} ('{new_name.strip()}') updated successfully in MySQL database!")
                        st.rerun()
                    else:
                        st.error(f"❌ Failed to update product: {msg}")

            if submitted_cancel:
                st.session_state.editing_product = None
                st.rerun()

        st.markdown("</div>", unsafe_allow_html=True)

    # 4. CATEGORY-WISE PRODUCT DISPLAY
    st.markdown(
        """
        <div style="font-family:'Poppins', sans-serif; font-size: 1.5rem; font-weight: 800; color: #1B4D3E; margin-bottom: 1.2rem;">
            Category-wise Product Catalog
        </div>
        """,
        unsafe_allow_html=True
    )

    # Group products by Category
    grouped_products = {}
    for cat in db_categories:
        c_id = cat["category_id"]
        c_name = cat["category_name"]
        cat_prods = [p for p in db_products if p.get("category_id") == c_id]
        grouped_products[c_name] = cat_prods

    # Include products with missing or uncategorized IDs if any
    all_cat_ids = {c["category_id"] for c in db_categories}
    uncategorized = [p for p in db_products if p.get("category_id") not in all_cat_ids]
    if uncategorized:
        grouped_products["Other Products"] = uncategorized

    # Render products category by category
    for cat_name, prods in grouped_products.items():
        st.markdown(
            f"""
            <div style="
                background: #F8FAF8;
                border-left: 6px solid #16A34A;
                border-radius: 12px;
                padding: 10px 16px;
                margin-top: 1.5rem;
                margin-bottom: 1rem;
                box-shadow: 0 2px 8px rgba(0, 0, 0, 0.03);
            ">
                <span style="font-family:'Poppins', sans-serif; font-size: 1.25rem; font-weight: 800; color: #1B4D3E;">
                    📂 {cat_name}
                </span>
                <span style="background: #DCFCE7; color: #166534; font-size: 0.8rem; font-weight: 700; padding: 3px 10px; border-radius: 12px; margin-left: 12px;">
                    {len(prods)} Products
                </span>
            </div>
            """,
            unsafe_allow_html=True
        )

        if not prods:
            st.info(f"No products found in category '{cat_name}'.")
            continue

        # Prepare product display table and edit action button
        for p in prods:
            p_id = p.get("product_id")
            p_name = p.get("product_name", "Organic Item")
            price = float(p.get("price") or 0.0)
            disc = float(p.get("discount") or 0.0)
            final_price = round(price - (price * (disc / 100.0)), 2)
            unit = p.get("unit") or "kg"
            qty = p.get("quantity") or 50
            mfg = str(p.get("manufacture_date") or "2026-07-20")
            exp = str(p.get("expiry_date") or "2026-08-05")

            p_col1, p_col2, p_col3, p_col4, p_col5, p_col6 = st.columns([1, 3.2, 1.8, 1.8, 1.8, 1.2])

            with p_col1:
                st.markdown(f"<b>#{p_id}</b>", unsafe_allow_html=True)
            with p_col2:
                st.markdown(f"<b>{p_name}</b><br><span style='font-size:0.78rem; color:#64748B;'>Stock: {qty} {unit} | Mfg: {mfg} | Exp: {exp}</span>", unsafe_allow_html=True)
            with p_col3:
                st.markdown(f"<span style='color:#64748B;'>Price:</span> <s>{CURRENCY}{price:,.2f}</s>", unsafe_allow_html=True)
            with p_col4:
                st.markdown(f"<span style='background:#FEE2E2; color:#991B1B; padding:2px 8px; border-radius:8px; font-weight:700; font-size:0.82rem;'>{disc:.0f}% OFF</span>", unsafe_allow_html=True)
            with p_col5:
                st.markdown(f"<b style='color:#16A34A; font-size:1.05rem;'>{CURRENCY}{final_price:,.2f} / {unit}</b>", unsafe_allow_html=True)
            with p_col6:
                if st.button("✏️ Edit", key=f"edit_btn_{p_id}", use_container_width=True):
                    st.session_state.editing_product = p
                    st.rerun()

            st.markdown("<hr style='border:0; height:1px; background:#F0F4F1; margin: 6px 0 10px 0;'>", unsafe_allow_html=True)
