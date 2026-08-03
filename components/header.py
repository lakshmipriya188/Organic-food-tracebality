"""Header and Navigation bar component for Organic Foods."""

import streamlit as st
from config import HELPLINE, APP_NAME, APP_SUBTITLE
from utils.cart_manager import _init_state, go_to, cart_count, wishlist_items
from products import get_all_categories


def render_header():
    """Render Organic Foods modern header and sub-navigation bar."""
    _init_state()

    # MAIN HEADER ROW (Brand, Search, Actions)
    col_brand, col_search, col_actions = st.columns([3.0, 4.2, 4.8])

    # 1. Brand Logo & Subtitle
    with col_brand:
        st.markdown(
            f"""
            <div style="cursor:pointer; display:inline-block;" onclick="window.location.reload();">
                <div style="display:flex; align-items:center; gap:10px;">
                    <div style="
                        background: linear-gradient(135deg, #22C55E 0%, #15803D 100%);
                        color: #FFFFFF;
                        width: 44px;
                        height: 44px;
                        border-radius: 14px;
                        display: flex;
                        align-items: center;
                        justify-content: center;
                        font-size: 1.5rem;
                        box-shadow: 0 4px 14px rgba(34, 197, 94, 0.25);
                    ">🌱</div>
                    <div>
                        <div style="font-family:'Poppins', sans-serif; font-size: 1.9rem; font-weight: 800; color: #1B4D3E; line-height: 1.0; letter-spacing: -0.5px;">
                            {APP_NAME}
                        </div>
                        <div style="font-family:'Poppins', sans-serif; font-size: 0.65rem; font-weight: 700; color: #16A34A; letter-spacing: 2.5px; margin-top: 3px; text-transform: uppercase;">
                            {APP_SUBTITLE}
                        </div>
                    </div>
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
            placeholder="🔍 Search organic rice, ghee, millets, cold pressed oils...",
            label_visibility="collapsed",
            key="header_search_input"
        )
        if search_val != st.session_state.search_query:
            st.session_state.search_query = search_val
            if search_val.strip():
                go_to("search")
                st.rerun()

    # 3. Header Actions: Wishlist, Cart, Account
    with col_actions:
        w_count = len(wishlist_items())
        c_count = cart_count()

        w_label = f"❤️ Wishlist ({w_count})" if w_count > 0 else "🤍 Wishlist"
        c_label = f"🛒 Cart ({c_count})" if c_count > 0 else "🛒 Cart"
        user_name = st.session_state.user.split(" ")[0] if st.session_state.user else "Log in"
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

    st.markdown("<div style='margin-bottom: 0.6rem;'></div>", unsafe_allow_html=True)

    # SUB-NAVBAR ROW (Browse Categories, Store Locations)
    sub_col1, sub_col2, _ = st.columns([3.5, 1.8, 4.7])

    # Browse Categories Dropdown
    with sub_col1:
        categories_list = get_all_categories()
        cat_name_map = {c.name: c for c in categories_list}
        selected_cat = st.selectbox(
            "Browse Categories",
            options=["🌿 Browse All Categories"] + list(cat_name_map.keys()),
            label_visibility="collapsed",
            key="cat_dropdown"
        )
        if selected_cat != "🌿 Browse All Categories":
            cat_obj = cat_name_map.get(selected_cat)
            if cat_obj:
                st.session_state["active_category_id"] = cat_obj.category_id
                go_to("category", active_category=cat_obj.slug)
                st.rerun()

    # Store Locations Link
    with sub_col2:
        if st.button("📍 Stores", key="nav_stores", use_container_width=True):
            go_to("store_locations")
            st.rerun()

    st.markdown("<hr style='border:0; height:1px; background:#E2E9E3; margin: 0.8rem 0 1.5rem 0;'>", unsafe_allow_html=True)
