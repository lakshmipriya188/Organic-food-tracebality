"""Admin Portal Page Component for Organic Foods."""

import streamlit as st
from utils.cart_manager import go_to


def render_admin_page():
    """Render Admin Page placeholder with administrative layout."""
    
    # Navigation header row
    col_back, _ = st.columns([2, 8])
    with col_back:
        if st.button("← Back to Store", key="admin_back_btn"):
            go_to("home")
            st.rerun()

    # Hero / Banner section for Admin Page
    st.markdown(
        """
        <div style="
            background: linear-gradient(135deg, #0F291E 0%, #1B4D3E 60%, #16A34A 100%);
            border-radius: 20px;
            padding: 2.2rem 2rem;
            color: #FFFFFF;
            box-shadow: 0 15px 35px rgba(27, 77, 62, 0.2);
            margin-bottom: 2rem;
        ">
            <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:1rem;">
                <div>
                    <span style="background: rgba(34, 197, 94, 0.25); color: #86EFAC; font-size: 0.75rem; font-weight: 800; padding: 4px 14px; border-radius: 20px; border: 1px solid rgba(134, 239, 172, 0.4); text-transform: uppercase; letter-spacing: 1.5px;">
                        🛡️ Admin Portal & Control Desk
                    </span>
                    <h1 style="font-family:'Poppins', sans-serif; color: #FFFFFF !important; margin: 0.6rem 0 0.2rem 0; font-size: 2.2rem;">
                        Admin Dashboard
                    </h1>
                    <p style="color: #E2E8F0; margin: 0; font-size: 0.95rem;">
                        Welcome to the central administrative panel. You are logged in with admin privileges.
                    </p>
                </div>
                <div style="text-align:right;">
                    <span style="font-size: 3rem;">⚙️</span>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Placeholder Admin Dashboard Content
    st.markdown(
        """
        <div style="
            background: #FFFFFF;
            border: 1px solid #E2E9E3;
            border-radius: 20px;
            padding: 2.5rem;
            text-align: center;
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.04);
            margin-bottom: 2rem;
        ">
            <div style="font-size: 3.5rem; margin-bottom: 0.8rem;">📦</div>
            <div style="font-family: 'Poppins', sans-serif; font-size: 1.6rem; font-weight: 700; color: #1B4D3E; margin-bottom: 0.5rem;">
                Admin Control Page
            </div>
            <div style="color: #4A6B5D; max-width: 600px; margin: 0 auto 1.5rem auto; font-size: 0.95rem; line-height: 1.6;">
                This page is reserved for future administrative tools and management modules. As requested, the admin user has full access to the customer store view along with the <b>🛡️ Admin</b> top navigation button to switch to this page at any time.
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Summary Stats / Overview Cards (Placeholder)
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric(label="Total Products", value="73", delta="Active in Catalog")
    with col2:
        st.metric(label="Categories", value="10", delta="Pure Organic")
    with col3:
        st.metric(label="System Status", value="Online", delta="MySQL & Streamlit")
    with col4:
        st.metric(label="Admin Access", value="Active", delta="Logged In")
