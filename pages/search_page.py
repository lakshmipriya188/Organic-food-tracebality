"""Search results page."""

import streamlit as st
from utils.cart_manager import go_to
from products import search_products
from components.product_card import render_product_card


def render_search_page():
    if st.button("← Back to home"):
        go_to("home")
        st.rerun()

    query = st.session_state.get("search_query", "")
    st.markdown('<div style="font-size:0.85rem; font-weight:800; color:#00472B; letter-spacing:2px;">SEARCH RESULTS</div>', unsafe_allow_html=True)
    st.markdown(f'<div style="font-size:2rem; font-weight:800; color:#00472B; margin-bottom:1.5rem;">Results for "{query}"</div>', unsafe_allow_html=True)

    results = search_products(query)
    if not results:
        st.warning(f"No products found matching '{query}'. Try searching for 'rice', 'ghee', 'oil', or 'millet'.")
        return

    cols = st.columns(min(len(results), 4))
    for i, p in enumerate(results):
        with cols[i % 4]:
            render_product_card(p, key_prefix="search_pg")
