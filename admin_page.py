"""Admin Portal Page Component for Organic Foods."""

import streamlit as st
from utils.cart_manager import go_to
from dashboard import render_dashboard


def render_admin_page():
    """Render Admin Portal Page using dashboard.py."""
    
    # Navigation header bar with Back to Store action
    col_back, _ = st.columns([2, 8])
    with col_back:
        if st.button("← Back to Organic Store", key="admin_back_btn"):
            go_to("home")
            st.rerun()

    # Call render_dashboard from dashboard.py
    render_dashboard()
