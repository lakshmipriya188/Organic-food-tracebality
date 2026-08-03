"""Hero banner component for Organic Foods."""

import streamlit as st
from utils.cart_manager import go_to
from utils.image_utils import get_image_src


def render_hero_banner():
    """Render the hero section with organic produce showcase and value prop strip."""
    
    # Outer Hero Container
    st.markdown(
        """
        <div style="
            background: linear-gradient(135deg, #0F382C 0%, #1B4D3E 50%, #166534 100%);
            border-radius: 24px;
            padding: 3.2rem 3rem 2.5rem 3rem;
            margin-bottom: 0px;
            position: relative;
            box-shadow: 0 15px 35px rgba(15, 56, 44, 0.2);
            color: #FFFFFF;
            overflow: hidden;
        ">
        """,
        unsafe_allow_html=True
    )

    h_col1, h_col2 = st.columns([1.1, 1.2])

    with h_col1:
        st.markdown(
            """
            <div style="
                display: inline-block;
                background: rgba(34, 197, 94, 0.2);
                border: 1px solid rgba(34, 197, 94, 0.4);
                padding: 4px 14px;
                border-radius: 20px;
                font-size: 0.78rem;
                font-weight: 800;
                color: #86EFAC;
                letter-spacing: 2px;
                text-transform: uppercase;
                margin-bottom: 1.2rem;
            ">
                🌱 100% CERTIFIED PURE ORGANIC
            </div>
            <div style="font-family: 'Poppins', sans-serif; font-size: 2.8rem; font-weight: 800; color: #FFFFFF; line-height: 1.15; letter-spacing: -0.5px; margin-bottom: 1.2rem;">
                Pure Organic Foods,<br><span style="color: #86EFAC;">Direct From Farm To Fork.</span>
            </div>
            <div style="font-size: 1.05rem; color: #E2E8F0; line-height: 1.6; margin-bottom: 2rem; max-width: 500px;">
                Experience the authentic taste of unadulterated nature across our 10 certified organic categories — harvested at peak nutrition with full batch traceability.
            </div>
            """,
            unsafe_allow_html=True
        )

        if st.button("🌿 Explore Fresh Organic Harvest", key="hero_shop_all_btn"):
            go_to("home")
            st.rerun()

    with h_col2:
        # 4 Organic Category Cards Showcase with glassmorphism
        m_col1, m_col2, m_col3, m_col4 = st.columns(4)
        
        pouches = [
            ("Fruits", "Fresh Organic", get_image_src("assets/images/fruits.jpg")),
            ("Vegetables", "Farm Fresh", get_image_src("assets/images/vegetables.jpg")),
            ("Millets", "Ancient Grains", get_image_src("assets/images/millets.jpg")),
            ("Oils", "Pure Ghani", get_image_src("assets/images/oils.jpg")),
        ]

        for col, (name, size, img_src) in zip([m_col1, m_col2, m_col3, m_col4], pouches):
            with col:
                st.markdown(
                    f"""
                    <div style="
                        background: rgba(255, 255, 255, 0.12);
                        backdrop-filter: blur(12px);
                        -webkit-backdrop-filter: blur(12px);
                        border: 1px solid rgba(255, 255, 255, 0.25);
                        border-radius: 18px;
                        padding: 0.8rem;
                        text-align: center;
                        box-shadow: 0 10px 25px rgba(0, 0, 0, 0.15);
                        transition: transform 0.3s ease;
                    ">
                        <img src="{img_src}" style="width: 100%; height: 130px; object-fit: cover; border-radius: 12px; margin-bottom: 8px;">
                        <div style="font-size: 0.82rem; font-weight: 800; color: #FFFFFF; text-transform: uppercase; letter-spacing: 0.5px;">{name}</div>
                        <div style="font-size: 0.72rem; color: #86EFAC; font-weight: 600;">{size}</div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

    st.markdown("</div>", unsafe_allow_html=True)

    # Bottom Organic Feature Strip
    st.markdown(
        """
        <div style="
            background-color: #166534;
            border-radius: 0 0 20px 20px;
            padding: 1rem 2rem;
            margin-top: -15px;
            margin-bottom: 2.5rem;
            color: #FFFFFF;
            display: flex;
            justify-content: space-around;
            align-items: center;
            font-size: 0.85rem;
            font-weight: 700;
            letter-spacing: 1px;
            box-shadow: 0 4px 15px rgba(22, 101, 52, 0.2);
            flex-wrap: wrap;
            gap: 10px;
        ">
            <div>⚡ 100% PESTICIDE-FREE</div>
            <div>🩺 NABL AUDITED LAB REPORTS</div>
            <div>👨‍🌾 DIRECT FARMER COOPERATIVE</div>
            <div>🚚 SAME-DAY EXPRESS HARVEST</div>
        </div>
        """,
        unsafe_allow_html=True
    )
