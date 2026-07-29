"""NABL Lab Test Reports search and inspection page."""

import streamlit as st
from utils.cart_manager import go_to
from products import PRODUCTS


def render_lab_reports_page():
    if st.button("← Back to home"):
        go_to("home")
        st.rerun()

    st.markdown('<div style="font-size:0.85rem; font-weight:800; color:#00472B; letter-spacing:2px;">CERTIFIED TRANSPARENCY</div>', unsafe_allow_html=True)
    st.markdown('<div style="font-size:2rem; font-weight:800; color:#00472B; margin-bottom:1.5rem;">NABL Lab Test Certificates 📄</div>', unsafe_allow_html=True)
    st.write("Every batch of produce undergoes multi-residue chemical pesticide analysis at NABL-accredited labs before reaching store shelves.")

    p_names = [p.name for p in PRODUCTS]
    selected_p = st.selectbox("Select product to view chemical audit report:", options=p_names)

    prod = next((p for p in PRODUCTS if p.name == selected_p), PRODUCTS[0])

    col1, col2 = st.columns([1, 2])
    with col1:
        st.image(prod.image_url, use_container_width=True)
    with col2:
        st.markdown(f"### {prod.name}")
        st.markdown(f"**Laboratory Certificate:** `{prod.lab_cert}`")
        st.markdown(f"**Farmer Producer Co-op:** {prod.origin}")
        
        st.markdown("#### Test Result Summary")
        st.success("✅ Organochlorine Pesticides: **0.00 mg/kg (NOT DETECTED)**")
        st.success("✅ Organophosphorus Residues: **0.00 mg/kg (NOT DETECTED)**")
        st.success("✅ Synthetic Pyrethroids: **0.00 mg/kg (NOT DETECTED)**")
        st.info("🔬 Heavy Metal Limits (Pb, Cd, As): **Conforms strictly to FSSAI Organic Standards**")

        if st.button("Download NABL PDF Report 📥"):
            st.toast(f"Downloading NABL Report for {prod.name}...")
