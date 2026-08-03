import streamlit as st
from products import get_products_by_tag, get_bestseller_products, get_deals_products, get_new_arrivals_products
from components.product_card import render_product_card
from utils.cart_manager import _init_state

TAB_MAP = {
    "Bestsellers": "bestseller",
    "Deals": "deal",
    "New Arrivals": "new",
}


def render_favourites():
    """Render Customer favourites section with Bestsellers / Deals / New Arrivals tabs."""
    _init_state()

    head_col, tab_col = st.columns([2.5, 2.5])

    with head_col:
        st.markdown(
            """
            <div style="font-family: 'Poppins', sans-serif; font-size: 0.82rem; font-weight: 700; color: #16A34A; letter-spacing: 2px; text-transform: uppercase; margin-bottom: 4px;">
                FEATURED HARVEST
            </div>
            <div style="font-family: 'Poppins', sans-serif; font-size: 2rem; font-weight: 700; color: #1B4D3E; margin-bottom: 1.5rem;">
                Customer Favourites ❤️
            </div>
            """,
            unsafe_allow_html=True
        )

    with tab_col:
        # Tab Buttons Top Right
        t_cols = st.columns(len(TAB_MAP))
        current_tab = st.session_state.get("fav_tab", "Bestsellers")

        for col, (display_name, tag_key) in zip(t_cols, TAB_MAP.items()):
            with col:
                is_active = (current_tab == display_name)
                btn_label = f"✨ {display_name}" if is_active else display_name
                if st.button(btn_label, key=f"fav_tab_{tag_key}", use_container_width=True):
                    st.session_state.fav_tab = display_name
                    st.rerun()

    # Get Products matching active tab tag
    active_tab_name = st.session_state.get("fav_tab", "Bestsellers")
    active_tag = TAB_MAP.get(active_tab_name, "bestseller")

    if active_tab_name == "Bestsellers":
        fav_products = get_bestseller_products()
    elif active_tab_name == "Deals":
        fav_products = get_deals_products()
    elif active_tab_name == "New Arrivals":
        fav_products = get_new_arrivals_products()
    else:
        fav_products = get_products_by_tag(active_tag)

    # 5 Columns for Product Cards
    num_cols = min(len(fav_products), 5)
    if num_cols > 0:
        cols = st.columns(num_cols)
        for i, product in enumerate(fav_products[:5]):
            with cols[i]:
                render_product_card(product, key_prefix=f"fav_{active_tag}")

    st.markdown("<div style='margin-bottom: 2.5rem;'></div>", unsafe_allow_html=True)