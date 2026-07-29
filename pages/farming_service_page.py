"""Farming As A Service overview for partner farmers."""

import streamlit as st
from utils.cart_manager import go_to


def render_farming_service_page():
    if st.button("← Back to home"):
        go_to("home")
        st.rerun()

    st.markdown('<div style="font-size:0.85rem; font-weight:800; color:#00472B; letter-spacing:2px;">FARMER PRODUCER CO-OP</div>', unsafe_allow_html=True)
    st.markdown('<div style="font-size:2rem; font-weight:800; color:#00472B; margin-bottom:1.5rem;">Farming As A Service (FAAS) 🌾</div>', unsafe_allow_html=True)
    
    st.markdown(
        """
        We empower over 12,000+ organic farmers in Mandya and surrounding districts through our end-to-end Farming As A Service program:
        
        - 🧬 **Native Heritage Seed Bank:** Free supply of heirloom non-hybrid seeds (Ragi, Rajamudi, Foxtail).
        - 🧪 **Soil & Water Testing:** Free bi-annual soil health cards and microbial analysis.
        - 🌾 **Organic Certification Assistance:** Full guidance for NPOP & Jaivik Bharat organic certification.
        - 💰 **Guaranteed Buyback Guarantee:** Fair price remuneration paid directly into farmer bank accounts within 48 hours.
        """
    )

    st.markdown("### Join as a Partner Farmer")
    with st.form("farmer_join_form"):
        name = st.text_input("Farmer Full Name")
        phone = st.text_input("Mobile Number")
        village = st.text_input("Village / District")
        acres = st.number_input("Land Size (in Acres)", min_value=1, max_value=50, value=5)
        submitted = st.form_submit_button("Submit Enrollment Request", use_container_width=True)
        if submitted:
            if name and phone and village:
                st.success(f"Thank you {name}! Our Mandya Agriculture Officer will contact you within 24 hours.")
            else:
                st.error("Please fill in all mandatory fields.")
