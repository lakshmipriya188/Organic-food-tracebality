"""Classic Header and Navigation bar component for Organic Mandya."""

import streamlit as st
from config import HELPLINE
from utils.cart_manager import _init_state, go_to, cart_count, wishlist_items
from products import CATEGORIES


def render_header():
    """Render Organic Mandya clean classic header and sub-navigation bar."""
    _init_state()

    # TOP HEADER ROW
    col_brand, col_search, col_pincode, col_actions = st.columns([2.8, 3.5, 2.2, 3])

    # 1. Brand Logo (Classic Serif + Clean Subtitle)
    with col_brand:
        st.markdown(
            """
            <div style="cursor:pointer;" onclick="window.location.reload();">
                <div style="font-family:'Georgia', serif; font-size:2.1rem; font-weight:800; color:#00472B; line-height:1.0; letter-spacing:-0.5px;">
                    Organic Mandya
                </div>
                <div style="font-size:0.68rem; font-weight:700; color:#556B60; letter-spacing:3.5px; margin-top:4px;">
                    PURE ROOTS · 100% ORGANIC
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    # 2. Search Input
    with col_search:
        search_val = st.text_input(
            "Search",
            value=st.session_state.get("search_query", ""),
            placeholder="Search organic rice, ghee, millets, oils...",
            label_visibility="collapsed",
            key="header_search_input"
        )
        if search_val != st.session_state.search_query:
            st.session_state.search_query = search_val
            if search_val.strip():
                go_to("search")
                st.rerun()

    # 3. Deliver to Pincode Box
    with col_pincode:
        pin = st.text_input(
            "Pincode",
            value=f"📍 Deliver to {st.session_state.deliver_pincode}",
            label_visibility="collapsed",
            key="pincode_display"
        )

    # 4. Header Actions: Wishlist, Cart, Account
    with col_actions:
        w_count = len(wishlist_items())
        c_count = cart_count()

        w_label = f"♡ Wishlist ({w_count})" if w_count > 0 else "♡ Wishlist"
        c_label = f"🛒 Cart ({c_count})" if c_count > 0 else "🛒 Cart"
        user_name = st.session_state.user.split("@")[0] if st.session_state.user else "Log in"
        u_label = f"👤 {user_name}"

        act_col1, act_col2, act_col3 = st.columns(3)
        with act_col1:
            if st.button(w_label, key="hdr_wish_btn", use_container_width=True):
                go_to("wishlist")
                st.rerun()
        with act_col2:
            if st.button(c_label, key="hdr_cart_btn", use_container_width=True):
                go_to("cart")
                st.rerun()
        with act_col3:
            if st.button(u_label, key="hdr_user_btn", use_container_width=True):
                go_to("account")
                st.rerun()

    st.markdown("<div style='margin-bottom: 0.8rem;'></div>", unsafe_allow_html=True)

    # SUB-NAVBAR ROW (Cleaned: Browse Categories, Store Locations, Deals, Customer Helpline)
    sub_col1, sub_col2, sub_col3, sub_col4 = st.columns([3, 1.8, 1.6, 3.6])

    # Browse All Categories Dropdown
    with sub_col1:
        selected_cat = st.selectbox(
            "Browse Categories",
            options=["🟢 Browse All Categories"] + [c.name for c in CATEGORIES],
            label_visibility="collapsed",
            key="cat_dropdown"
        )
        if selected_cat != "🟢 Browse All Categories":
            cat_obj = next((c for c in CATEGORIES if c.name == selected_cat), None)
            if cat_obj:
                go_to("category", active_category=cat_obj.slug)
                st.rerun()

    # Store Locations Link
    with sub_col2:
        if st.button("Store Locations", key="nav_stores", use_container_width=True):
            go_to("store_locations")
            st.rerun()

    # Deals Link
    with sub_col3:
        if st.button("Deals", key="nav_deals", use_container_width=True):
            go_to("deals")
            st.rerun()

    # Customer Support Phone
    with sub_col4:
        st.markdown(
            f'<div style="text-align:right; font-weight:700; color:#00472B; font-size:0.95rem; padding-top:6px;">'
            f'🎧 Customer Support: {HELPLINE}</div>',
            unsafe_allow_html=True
        )

    st.markdown("<hr style='border:0; height:1px; background:#e2e8f0; margin: 0.8rem 0 1.5rem 0;'>", unsafe_allow_html=True)
