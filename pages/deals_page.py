"""Co-Op Member Deals and Offers page."""

import streamlit as st
from utils.cart_manager import go_to
from products import get_products_by_tag
from components.product_card import render_product_card


def render_deals_page():
    if st.button("← Back to home"):
        go_to("home")
        st.rerun()

    st.markdown('<div style="font-size:0.85rem; font-weight:800; color:#00472B; letter-spacing:2px;">EXCLUSIVE OFFERS</div>', unsafe_allow_html=True)
    st.markdown('<div style="font-size:2rem; font-weight:800; color:#00472B; margin-bottom:1.5rem;">Co-Op Member Deals & Discounts 🏷️</div>', unsafe_allow_html=True)

    deals_products = get_products_by_tag("deal")
    if not deals_products:
        st.info("No active promotional deals right now. Check back soon!")
        return

    cols = st.columns(min(len(deals_products), 4))
    for i, p in enumerate(deals_products):
        with cols[i % 4]:
            render_product_card(p, key_prefix="deals_pg")
