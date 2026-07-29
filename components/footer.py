"""Footer component matching clean classic organic layout."""

import streamlit as st
from config import HELPLINE, APP_NAME, APP_SUBTITLE
from utils.cart_manager import go_to


def render_footer():
    """Render clean classic footer and back-to-top floating button."""
    
    st.markdown("<hr style='border:0; height:1px; background:#e2e8f0; margin: 3rem 0 2rem 0;'>", unsafe_allow_html=True)

    f_col1, f_col2, f_col3, f_col4 = st.columns([2, 1.3, 1.3, 1.6])

    with f_col1:
        st.markdown(
            f"""
            <div style="font-family:'Georgia', serif; font-size:1.7rem; font-weight:800; color:#00472B;">
                {APP_NAME}
            </div>
            <div style="font-size:0.7rem; font-weight:700; color:#556B60; letter-spacing:3px; margin-bottom:1rem;">
                {APP_SUBTITLE}
            </div>
            <div style="font-size:0.9rem; color:#4A5D54; line-height:1.5; max-width:320px;">
                Direct farmer co-operative producing 100% certified organic staples, ancient millets, and Bilona cow ghee from Mandya, Karnataka.
            </div>
            """,
            unsafe_allow_html=True
        )

    with f_col2:
        st.markdown("<div style='font-weight:800; color:#00472B; margin-bottom:0.8rem;'>Categories</div>", unsafe_allow_html=True)
        if st.button("Ancient Millets", key="ftr_millet"):
            go_to("category", active_category="millets")
            st.rerun()
        if st.button("A2 Desi Ghee", key="ftr_ghee"):
            go_to("category", active_category="dairy")
            st.rerun()
        if st.button("Cold Pressed Oils", key="ftr_oils"):
            go_to("category", active_category="cold-pressed-oils")
            st.rerun()

    with f_col3:
        st.markdown("<div style='font-weight:800; color:#00472B; margin-bottom:0.8rem;'>Stores & Deals</div>", unsafe_allow_html=True)
        if st.button("Store Locations 📍", key="ftr_stores"):
            go_to("store_locations")
            st.rerun()
        if st.button("Special Deals 🏷️", key="ftr_deals"):
            go_to("deals")
            st.rerun()

    with f_col4:
        st.markdown("<div style='font-weight:800; color:#00472B; margin-bottom:0.8rem;'>Customer Helpline</div>", unsafe_allow_html=True)
        st.markdown(
            f"""
            <div style="font-size: 1.1rem; font-weight: 800; color: #00472B; margin-bottom: 0.5rem;">
                🎧 {HELPLINE}
            </div>
            <div style="font-size: 0.85rem; color: #556B60;">
                Mon - Sat: 9:00 AM to 8:00 PM IST<br>
                Mandya Organic Farmer Collective
            </div>
            """,
            unsafe_allow_html=True
        )

    # Back to top button row
    st.markdown("<div style='margin-top:2rem;'></div>", unsafe_allow_html=True)
    top_c1, top_c2 = st.columns([8, 1])
    with top_c2:
        if st.button("↑ Top", key="back_to_top_btn", use_container_width=True):
            st.rerun()

    st.markdown(
        """
        <div style="text-align: center; font-size: 0.8rem; color: #888888; margin-top: 1.5rem; padding-bottom: 1rem;">
            © Organic Mandya Pure Roots · 100% Certified Organic Produce. All rights reserved.
        </div>
        """,
        unsafe_allow_html=True
    )
