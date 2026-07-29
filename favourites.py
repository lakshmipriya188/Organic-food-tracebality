"""Customer favourites section matching Organic Mandya reference Image 3."""

import streamlit as st
from products import get_products_by_tag
from components.product_card import render_product_card
from utils.cart_manager import _init_state

TAB_MAP = {
    "Bestsellers": "bestseller",
    "Deals": "deal",
    "New": "new",
}


def render_favourites():
    """Render Customer favourites section with Bestsellers / Deals / New tabs."""
    _init_state()

    head_col, tab_col = st.columns([2.5, 2])

    with head_col:
        st.markdown(
            """
            <div style="font-size: 0.85rem; font-weight: 800; color: #00472B; letter-spacing: 2px; text-transform: uppercase; margin-bottom: 2px;">
                SHOP
            </div>
            <div style="font-size: 2rem; font-weight: 800; color: #00472B; margin-bottom: 1.5rem;">
                Customer favourites
            </div>
            """,
            unsafe_allow_html=True
        )

    with tab_col:
        # Tab Buttons Top Right
        t_cols = st.columns(len(TAB_MAP))
        current_tab = st.session_state.get("fav_tab", "Bestsellers")

        for col, tab_name in zip(t_cols, TAB_MAP.keys()):
            with col:
                is_active = (current_tab == tab_name)
                btn_style = f"""
                <div style="text-align: right;">
                    <span style="
                        font-weight: 800;
                        color: {'#00472B' if is_active else '#666666'};
                        border-bottom: {'3px solid #00472B' if is_active else 'none'};
                        padding-bottom: 4px;
                        cursor: pointer;
                    ">
                        {tab_name}
                    </span>
                </div>
                """
                if st.button(tab_name, key=f"fav_tab_{tab_name}", use_container_width=True):
                    st.session_state.fav_tab = tab_name
                    st.rerun()

    # Get Products matching active tab tag
    tag = TAB_MAP.get(st.session_state.get("fav_tab", "Bestsellers"), "bestseller")
    fav_products = get_products_by_tag(tag)

    # 5 Columns for Product Cards (matching Image 3)
    num_cols = min(len(fav_products), 5)
    cols = st.columns(num_cols)

    for i, product in enumerate(fav_products[:5]):
        with cols[i]:
            render_product_card(product, key_prefix=f"fav_{tag}")

    st.markdown("<div style='margin-bottom: 2.5rem;'></div>", unsafe_allow_html=True)