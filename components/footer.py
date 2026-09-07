"""Footer component matching clean classic organic layout for Farmora."""

import streamlit as st
from config import HELPLINE, APP_NAME, APP_SUBTITLE
from utils.cart_manager import go_to


def render_footer():
    """Render clean modern footer with Farmora branding and trust badges."""
    st.markdown("<hr style='border:0; height:1px; background:#E2E9E3; margin: 3.5rem 0 2rem 0;'>", unsafe_allow_html=True)

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
