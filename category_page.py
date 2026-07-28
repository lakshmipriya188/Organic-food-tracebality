"""Category detail page: shows all products belonging to the active category."""

import streamlit as st
from products import CATEGORIES, get_products_by_category
from components.product_card import render_product_card
from utils.cart_manager import go_to


def render_category_page():
    slug = st.session_state.get("active_category")
    category = next((c for c in CATEGORIES if c.slug == slug), None)

    if st.button("← Back to home"):
        go_to("home")
        st.rerun()

    if not category:
        st.warning("Category not found.")
        return

    st.markdown('<div class="om-section-heading">CATEGORY</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="om-section-title">{category.name}</div>', unsafe_allow_html=True)

    products = get_products_by_category(slug)
    if not products:
        st.info(
            f"We're still stocking the shelves for **{category.name}** — "
            "new products are added every week. Check back soon!"
        )
        return

    n_cols = min(len(products), 5)
    cols = st.columns(n_cols)
    for i, product in enumerate(products):
        with cols[i % n_cols]:
            render_product_card(product, key_prefix="catpage")
