"""Co-Op Member Deals and Offers page for Organic Foods."""

import streamlit as st
from utils.cart_manager import go_to
from products import get_deals_products, get_products_by_tag
from components.product_card import render_product_card


def render_deals_page():
    if st.button("← Back to home"):
        go_to("home")
        st.rerun()

    st.markdown(
        """
        <div style="font-family:'Poppins', sans-serif; font-size:0.82rem; font-weight:700; color:#16A34A; letter-spacing:2px; text-transform:uppercase; margin-bottom:4px;">
            EXCLUSIVE OFFERS
        </div>
        <div style="font-family:'Poppins', sans-serif; font-size:2rem; font-weight:700; color:#1B4D3E; margin-bottom:1.5rem;">
            Co-Op Member Deals & Discounts 🏷️
        </div>
        """,
        unsafe_allow_html=True
    )

    deals_products = get_deals_products()
    if not deals_products:
        st.info("No active promotional deals right now. Check back soon!")
        return

    cols = st.columns(min(len(deals_products), 4))
    for i, p in enumerate(deals_products):
        with cols[i % 4]:
            render_product_card(p, key_prefix="deals_pg")
