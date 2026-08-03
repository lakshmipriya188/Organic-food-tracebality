"""Search results page for Organic Foods."""

import streamlit as st
from utils.cart_manager import go_to
from products import search_products
from components.product_card import render_product_card


def render_search_page():
    if st.button("← Back to home"):
        go_to("home")
        st.rerun()

    query = st.session_state.get("search_query", "")
    st.markdown(
        f"""
        <div style="font-family:'Poppins', sans-serif; font-size:0.82rem; font-weight:700; color:#16A34A; letter-spacing:2px; text-transform:uppercase; margin-bottom:4px;">
            SEARCH RESULTS
        </div>
        <div style="font-family:'Poppins', sans-serif; font-size:2rem; font-weight:700; color:#1B4D3E; margin-bottom:1.5rem;">
            Results for "{query}"
        </div>
        """,
        unsafe_allow_html=True
    )

    results = search_products(query)
    if not results:
        st.warning(f"No products found matching '{query}'. Try searching for 'rice', 'ghee', 'oil', or 'millet'.")
        return

    cols = st.columns(min(len(results), 4))
    for i, p in enumerate(results):
        with cols[i % 4]:
            render_product_card(p, key_prefix="search_pg")
