"""Hero banner component matching Organic Mandya reference Image 1."""

import streamlit as st
from utils.cart_manager import go_to


def render_hero_banner():
    """Render the hero section with millet showcase and bottom value prop strip."""
    
    # Outer Hero Container
    st.markdown(
        """
        <div style="
            background: linear-gradient(135deg, #EBF5F0 0%, #D8EAE0 100%);
            border-radius: 24px;
            padding: 3rem 3rem 2rem 3rem;
            margin-bottom: 0px;
            position: relative;
            box-shadow: 0 4px 20px rgba(0, 71, 43, 0.05);
        ">
        """,
        unsafe_allow_html=True
    )

    h_col1, h_col2 = st.columns([1.1, 1.2])

    with h_col1:
        st.markdown(
            """
            <div style="font-size: 0.82rem; font-weight: 800; color: #00472B; letter-spacing: 2.5px; text-transform: uppercase; margin-bottom: 0.8rem;">
                ANCIENT GRAINS · MODERN PLATES
            </div>
            <div style="font-size: 2.8rem; font-weight: 800; color: #00472B; line-height: 1.15; letter-spacing: -1px; margin-bottom: 1.2rem;">
                Millets, the way<br>they were meant to<br>be.
            </div>
            <div style="font-size: 1.05rem; color: #4A5D54; line-height: 1.5; margin-bottom: 2rem; max-width: 480px;">
                Foxtail, Browntop, Ragi and Proso — single-origin millets grown by our farmer cooperative and milled fresh so the goodness stays in.
            </div>
            """,
            unsafe_allow_html=True
        )

        if st.button("Shop millets", key="hero_shop_millets_btn"):
            go_to("category", active_category="millets")
            st.rerun()

        st.markdown(
            """
            <div style="margin-top: 2rem; font-size: 0.9rem; color: #00472B; letter-spacing: 4px;">
                <span style="color:#00472B;">●</span> <span style="color:#A3C4B3;">○ ○ ○</span>
            </div>
            """,
            unsafe_allow_html=True
        )

    with h_col2:
        # 4 Millet Pouches Showcase
        m_col1, m_col2, m_col3, m_col4 = st.columns(4)
        
        pouches = [
            ("Foxtail Millet", "500g", "https://images.unsplash.com/photo-1615485290382-441e4d049cb5?w=300&auto=format&fit=crop&q=80"),
            ("Browntop Millet", "500g", "https://images.unsplash.com/photo-1586201375761-83865001e31c?w=300&auto=format&fit=crop&q=80"),
            ("Ragi", "1kg", "https://images.unsplash.com/photo-1586201375761-83865001e31c?w=300&auto=format&fit=crop&q=80"),
            ("Proso Millet", "500g", "https://images.unsplash.com/photo-1615485290382-441e4d049cb5?w=300&auto=format&fit=crop&q=80"),
        ]

        for col, (name, size, img_url) in zip([m_col1, m_col2, m_col3, m_col4], pouches):
            with col:
                st.markdown(
                    f"""
                    <div style="
                        background: rgba(255,255,255,0.7);
                        backdrop-filter: blur(8px);
                        border: 1px solid rgba(255,255,255,0.8);
                        border-radius: 16px;
                        padding: 0.8rem;
                        text-align: center;
                        box-shadow: 0 8px 16px rgba(0,0,0,0.04);
                    ">
                        <img src="{img_url}" style="width: 100%; height: 130px; object-fit: cover; border-radius: 12px; margin-bottom: 8px;">
                        <div style="font-size: 0.78rem; font-weight: 800; color: #00472B; text-transform: uppercase;">{name}</div>
                        <div style="font-size: 0.7rem; color: #666;">{size}</div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

    st.markdown("</div>", unsafe_allow_html=True)

    # Bottom Dark Green Feature Strip (Image 1)
    st.markdown(
        """
        <div style="
            background-color: #00472B;
            border-radius: 0 0 20px 20px;
            padding: 0.9rem 2rem;
            margin-top: -15px;
            margin-bottom: 2.5rem;
            color: #FFFFFF;
            display: flex;
            justify-content: space-around;
            align-items: center;
            font-size: 0.85rem;
            font-weight: 700;
            letter-spacing: 1px;
        ">
            <div style="display:inline-block; margin-right: 2rem;">⚡ HIGH PROTEIN</div>
            <div style="display:inline-block; margin-right: 2rem;">🩺 LOW GLYCEMIC INDEX</div>
            <div style="display:inline-block;">👨‍🌾 SUPPORTS LOCAL FARMERS</div>
        </div>
        """,
        unsafe_allow_html=True
    )
