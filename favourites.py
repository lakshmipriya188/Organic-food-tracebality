"""'Customer favourites' section with tabbed filtering (Bestsellers/Deals/New)."""

import streamlit as st
from products import get_products_by_tag
from components.product_card import render_product_card
from utils.cart_manager import _init_state

TAB_TO_TAG = {"Bestsellers": "bestseller", "Deals": "deal", "New": "new"}


def render_favourites():
    _init_state()

    head_col, tab_col = st.columns([2.4, 2])
    with head_col:
        st.markdown('<div class="om-section-heading">SHOP</div>', unsafe_allow_html=True)
        st.markdown('<div class="om-section-title">Customer favourites</div>', unsafe_allow_html=True)

    with tab_col:
        t_cols = st.columns(len(TAB_TO_TAG))
        for col, tab_name in zip(t_cols, TAB_TO_TAG.keys()):
            with col:
                is_active = st.session_state.fav_tab == tab_name
                css_class = "om-tab-active" if is_active else "om-tab-inactive"
                st.markdown(f'<div class="{css_class}" style="text-align:right;">', unsafe_allow_html=True)
                if st.button(tab_name, key=f"tab_{tab_name}", use_container_width=True):
                    st.session_state.fav_tab = tab_name
                    st.rerun()
                st.markdown('</div>', unsafe_allow_html=True)

    products = get_products_by_tag(TAB_TO_TAG[st.session_state.fav_tab])
    if not products:
        st.info("No products in this section yet — check back soon!")
        return

    cols = st.columns(len(products) if len(products) <= 5 else 5)
    for col, product in zip(cols, products[:5]):
        with col:
            render_product_card(product, key_prefix="fav")
    st.write("")