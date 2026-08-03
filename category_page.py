"""Category detail page: shows products belonging strictly to the active MySQL Category table category_id."""

import streamlit as st
from products import get_all_categories, get_products_by_category_id
from components.product_card import render_product_card
from utils.cart_manager import go_to


def render_category_page():
    slug = st.session_state.get("active_category")
    active_cat_id = st.session_state.get("active_category_id")

    categories = get_all_categories()
    category = None

    if active_cat_id is not None:
        category = next((c for c in categories if c.category_id == active_cat_id), None)
    if not category and slug:
        category = next((c for c in categories if c.slug == slug), None)

    if st.button("← Back to home"):
        go_to("home")
        st.rerun()

    if not category:
        st.warning("Category not found.")
        return

    st.markdown(
        f"""
        <div style="
            background: linear-gradient(135deg, #1B4D3E 0%, #166534 100%);
            border-radius: 20px;
            padding: 2rem;
            color: #FFFFFF;
            margin-bottom: 2rem;
            box-shadow: 0 10px 25px rgba(27, 77, 62, 0.15);
        ">
            <div style="font-size: 0.8rem; font-weight: 800; color: #86EFAC; letter-spacing: 2px; text-transform: uppercase;">
                ORGANIC CATEGORY (ID: {category.category_id})
            </div>
            <div style="font-family: 'Poppins', sans-serif; font-size: 2.1rem; font-weight: 700; margin-top: 4px;">
                {category.name} 🌿
            </div>
            <div style="font-size: 0.95rem; color: #E2E8F0; margin-top: 6px;">
                {category.description} — 100% Certified Organic Harvest
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Query products strictly belonging to this category_id from MySQL Product table
    products = get_products_by_category_id(category.category_id)
    if not products:
        st.info(
            f"We're currently stocking the shelves for **{category.name}** (Category ID: {category.category_id}) — "
            "fresh harvests are added every week. Check back soon!"
        )
        return

    n_cols = min(len(products), 5)
    cols = st.columns(max(n_cols, 1))
    for i, product in enumerate(products):
        with cols[i % len(cols)]:
            render_product_card(product, key_prefix=f"catpage_{category.category_id}")
