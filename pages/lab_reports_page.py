"""NABL Lab Test Reports search and inspection page for Organic Foods."""

import streamlit as st
from utils.cart_manager import go_to
from products import PRODUCTS
from utils.image_utils import get_image_src


def render_lab_reports_page():
    if st.button("← Back to home"):
        go_to("home")
        st.rerun()

    st.markdown(
        """
        <div style="font-size:0.82rem; font-weight:800; color:#16A34A; letter-spacing:2.5px; text-transform:uppercase; margin-bottom:4px;">
            CERTIFIED TRANSPARENCY
        </div>
        <div style="font-size:2.2rem; font-weight:800; font-family:'Playfair Display', serif; color:#1B4D3E; margin-bottom:0.5rem;">
            NABL Lab Test Certificates 📄
        </div>
        <div style="color:#4A6B5D; margin-bottom:1.5rem; font-size:0.95rem;">
            Every batch of Organic Foods produce undergoes multi-residue chemical pesticide analysis at NABL-accredited labs before reaching store shelves.
        </div>
        """,
        unsafe_allow_html=True
    )

    p_names = [p.name for p in PRODUCTS]
    selected_p = st.selectbox("Select product to view chemical audit report:", options=p_names)

    prod = next((p for p in PRODUCTS if p.name == selected_p), PRODUCTS[0])
    img_src = get_image_src(prod.image_url)

    col1, col2 = st.columns([1, 2])
    with col1:
        st.markdown(
            f"""
            <img src="{img_src}" style="width: 100%; height: 220px; object-fit: cover; border-radius: 16px; border: 1px solid #E2E9E3;">
            """,
            unsafe_allow_html=True
        )
    with col2:
        st.markdown(f"<div style='font-family:\"Playfair Display\", serif; font-size: 1.6rem; font-weight: 800; color: #1B4D3E;'>{prod.name}</div>", unsafe_allow_html=True)
        st.markdown(f"**Laboratory Certificate:** `{prod.lab_cert}`")
        st.markdown(f"**Farmer Producer Co-op:** {prod.origin}")
        
        st.markdown("#### Test Result Summary")
        st.success("✅ Organochlorine Pesticides: **0.00 mg/kg (NOT DETECTED)**")
        st.success("✅ Organophosphorus Residues: **0.00 mg/kg (NOT DETECTED)**")
        st.success("✅ Synthetic Pyrethroids: **0.00 mg/kg (NOT DETECTED)**")
        st.info("🔬 Heavy Metal Limits (Pb, Cd, As): **Conforms strictly to FSSAI Organic Standards**")

        if st.button("Download NABL PDF Report 📥"):
            st.toast(f"Downloading NABL Report for {prod.name}...")
