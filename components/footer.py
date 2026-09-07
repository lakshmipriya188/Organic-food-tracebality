"""Footer component matching clean classic organic layout for Organic Foods."""

import streamlit as st
from config import HELPLINE, APP_NAME, APP_SUBTITLE
from utils.cart_manager import go_to


def render_footer():
    """Render clean modern footer with branding and quick links."""
    is_logged_in = bool(st.session_state.get("user"))

    st.markdown("<hr style='border:0; height:1px; background:#E2E9E3; margin: 3.5rem 0 2rem 0;'>", unsafe_allow_html=True)

    if not is_logged_in:
        # Pre-login Streamlined Footer: Only Farmora branding & trust badges
        st.markdown(
            f"""
<div style="
background: linear-gradient(135deg, #F4F8F5 0%, #EAF3ED 100%);
border: 1px solid #E2E9E3;
border-radius: 20px;
padding: 2rem 2.5rem;
text-align: center;
box-shadow: 0 4px 20px rgba(27, 77, 62, 0.03);
">
<div style="display: flex; align-items: center; justify-content: center; gap: 10px; margin-bottom: 8px;">
<div style="font-size: 1.8rem;">🌱</div>
<div style="font-family: 'Poppins', sans-serif; font-size: 1.8rem; font-weight: 800; color: #1B4D3E; letter-spacing: -0.5px;">
{APP_NAME}
</div>
</div>
<div style="font-family: 'Poppins', sans-serif; font-size: 0.72rem; font-weight: 800; color: #16A34A; letter-spacing: 3px; text-transform: uppercase; margin-bottom: 1rem;">
{APP_SUBTITLE}
</div>
<div style="font-size: 0.92rem; color: #4A6B5D; max-width: 620px; margin: 0 auto 1.5rem auto; line-height: 1.6;">
Direct farmer producer co-operative delivering 100% certified organic staples, ancient millets, cold pressed oils, and fresh farm produce with full batch traceability.
</div>
<div style="
display: flex;
justify-content: center;
align-items: center;
flex-wrap: wrap;
gap: 12px;
margin-bottom: 1.2rem;
">
<span style="background: #FFFFFF; border: 1px solid #D1E5D8; color: #166534; padding: 6px 16px; border-radius: 20px; font-size: 0.8rem; font-weight: 700; display: inline-flex; align-items: center; gap: 6px;">
🌿 100% Certified Organic
</span>
<span style="background: #FFFFFF; border: 1px solid #D1E5D8; color: #166534; padding: 6px 16px; border-radius: 20px; font-size: 0.8rem; font-weight: 700; display: inline-flex; align-items: center; gap: 6px;">
🌾 Direct Farmer Cooperative
</span>
<span style="background: #FFFFFF; border: 1px solid #D1E5D8; color: #166534; padding: 6px 16px; border-radius: 20px; font-size: 0.8rem; font-weight: 700; display: inline-flex; align-items: center; gap: 6px;">
🔍 Farm-to-Fork Traceability
</span>
</div>
</div>
<div style="text-align: center; font-size: 0.82rem; color: #7A9387; margin-top: 1.8rem; padding-bottom: 1rem;">
© {APP_NAME} Pure Roots · 100% Certified Organic Produce. All rights reserved.
</div>
""",
            unsafe_allow_html=True
        )
    else:
        # Full store footer when logged in
        f_col1, f_col2, f_col3, f_col4 = st.columns([2, 1.3, 1.3, 1.6])

        with f_col1:
            st.markdown(
                f"""
                <div style="display:flex; align-items:center; gap:8px; margin-bottom: 6px;">
                    <div style="font-size:1.6rem;">🌱</div>
                    <div style="font-family:'Poppins', sans-serif; font-size:1.6rem; font-weight:800; color:#1B4D3E;">
                        {APP_NAME}
                    </div>
                </div>
                <div style="font-family:'Poppins', sans-serif; font-size:0.65rem; font-weight:700; color:#16A34A; letter-spacing:2.5px; margin-bottom:1.2rem; text-transform:uppercase;">
                    {APP_SUBTITLE}
                </div>
                <div style="font-size:0.88rem; color:#4A6B5D; line-height:1.6; max-width:320px;">
                    Direct farmer producer co-operative delivering 100% certified organic staples, ancient millets, cold pressed oils, and A2 Bilona cow ghee straight from clean farms to your doorstep.
                </div>
                """,
                unsafe_allow_html=True
            )

        with f_col2:
            st.markdown("<div style='font-family:\"Poppins\", sans-serif; font-weight:700; color:#1B4D3E; margin-bottom:0.9rem; font-size:1rem;'>Organic Categories</div>", unsafe_allow_html=True)
            if st.button("Ancient Millets", key="ftr_millet"):
                go_to("category", active_category="millets")
                st.rerun()
            if st.button("A2 Desi Ghee", key="ftr_ghee"):
                go_to("category", active_category="dairy")
                st.rerun()
            if st.button("Cold Pressed Oils", key="ftr_oils"):
                go_to("category", active_category="oils")
                st.rerun()

        with f_col3:
            st.markdown("<div style='font-family:\"Poppins\", sans-serif; font-weight:700; color:#1B4D3E; margin-bottom:0.9rem; font-size:1rem;'>Quick Access</div>", unsafe_allow_html=True)
            if st.button("🤖 AI Predictor", key="ftr_ai_pred"):
                go_to("ml_prediction")
                st.rerun()
            if st.button("Store Locations 📍", key="ftr_stores"):
                go_to("store_locations")
                st.rerun()
            if st.button("Special Deals 🏷️", key="ftr_deals"):
                go_to("deals")
                st.rerun()
            if st.button("Farm Traceability 🌾", key="ftr_trace"):
                go_to("traceability")
                st.rerun()

        with f_col4:
            st.markdown("<div style='font-family:\"Poppins\", sans-serif; font-weight:700; color:#1B4D3E; margin-bottom:0.9rem; font-size:1rem;'>Customer Helpline</div>", unsafe_allow_html=True)
            st.markdown(
                f"""
                <div style="font-family:'Poppins', sans-serif; font-size: 1.1rem; font-weight: 700; color: #1B4D3E; margin-bottom: 0.5rem;">
                    🎧 <span style="color:#16A34A;">{HELPLINE}</span>
                </div>
                <div style="font-size: 0.85rem; color: #4A6B5D; line-height: 1.5;">
                    Mon - Sat: 8:00 AM to 9:00 PM IST<br>
                    {APP_NAME} Farmer Collective
                </div>
                """,
                unsafe_allow_html=True
            )

        st.markdown(
            f"""
            <div style="text-align: center; font-size: 0.82rem; color: #7A9387; margin-top: 2.5rem; padding-bottom: 1rem; border-top: 1px solid #E2E9E3; padding-top: 1.2rem;">
                © {APP_NAME} Pure Roots · 100% Certified Organic Produce. All rights reserved.
            </div>
            """,
            unsafe_allow_html=True
        )
