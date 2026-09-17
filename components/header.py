"""Header and Navigation bar component for Organic Foods."""

import streamlit as st
from config import HELPLINE, APP_NAME, APP_SUBTITLE
from utils.cart_manager import _init_state, go_to, cart_count, wishlist_count


def render_header():
    """Render Organic Foods clean header with Brand and Header Actions."""
    _init_state()

    # MAIN HEADER ROW (Brand Logo & Title on Left, Actions on Right)
    col_brand, col_actions = st.columns([4.2, 5.8])

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

    # 2. Header Actions: Login only when pre-login, full actions when logged in
    with col_actions:
        is_logged_in = bool(st.session_state.get("user"))
        is_admin = bool(st.session_state.get("is_admin", False))

        if not is_logged_in:
            # Pre-login navigation: Top login button removed as requested
            st.markdown(
                """
                <div style="text-align: right; font-family:'Poppins', sans-serif; font-size: 0.8rem; font-weight: 700; color: #16A34A; letter-spacing: 1px; padding: 6px 0;">
                    🌿 PURE ORGANIC HARVEST & TRACEABILITY
                </div>
                """,
                unsafe_allow_html=True
            )
        else:
            w_count = wishlist_count()
            c_count = cart_count()

            w_label = f"❤️ Wishlist ({w_count})" if w_count > 0 else "🤍 Wishlist"
            c_label = f"🛒 Cart ({c_count})" if c_count > 0 else "🛒 Cart"
            user_name = st.session_state.user.split(" ")[0] if st.session_state.user else "Log in"
            u_label = f"👤 {user_name}"

            act_col1, act_col2, act_col3, act_col4, act_col5 = st.columns([1.1, 1.2, 1.1, 1.8, 1.2])
            with act_col1:
                if st.button("📊 Admin", key="hdr_admin_btn", use_container_width=True):
                    go_to("admin")
                    st.rerun()
            with act_col2:
                if st.button(w_label, key="hdr_wish_btn", use_container_width=True):
                    go_to("wishlist")
                    st.rerun()
            with act_col3:
                if st.button(c_label, key="hdr_cart_btn", use_container_width=True):
                    go_to("cart")
                    st.rerun()
            with act_col4:
                if st.button("⚙️ Product Configurations", key="hdr_pconfig_btn", use_container_width=True):
                    go_to("product_config")
                    st.rerun()
            with act_col5:
                if st.button(u_label, key="hdr_user_btn", use_container_width=True):
                    go_to("account")
                    st.rerun()

    st.markdown("<hr style='border:0; height:1px; background:#E2E9E3; margin: 0.8rem 0 1.5rem 0;'>", unsafe_allow_html=True)
