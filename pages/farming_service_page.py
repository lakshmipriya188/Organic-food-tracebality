"""Farming As A Service overview for partner farmers."""

import streamlit as st
from utils.cart_manager import go_to


def render_farming_service_page():
    if st.button("← Back to home"):
        go_to("home")
        st.rerun()

    st.markdown(
        """
        <div style="font-size:0.82rem; font-weight:800; color:#16A34A; letter-spacing:2.5px; text-transform:uppercase; margin-bottom:4px;">
            FARMER PRODUCER CO-OP
        </div>
        <div style="font-size:2.2rem; font-weight:800; font-family:'Playfair Display', serif; color:#1B4D3E; margin-bottom:1.5rem;">
            Farming As A Service (FAAS) 🌾
        </div>
        """,
        unsafe_allow_html=True
    )
    
    st.markdown(
        """
        <div style="background:#FFFFFF; border:1px solid #E2E9E3; border-radius:18px; padding:1.5rem; margin-bottom:1.5rem; box-shadow:0 6px 18px rgba(27,77,62,0.04);">
            <div style="font-size:1.05rem; color:#0F291E; line-height:1.7;">
                We empower over 12,000+ organic farmers through our end-to-end <b>Organic Foods Farming As A Service</b> program:
                <br><br>
                <ul>
                    <li>🧬 <b>Native Heritage Seed Bank:</b> Free supply of heirloom non-hybrid seeds (Ragi, Rajamudi, Foxtail).</li>
                    <li>🧪 <b>Soil & Water Testing:</b> Free bi-annual soil health cards and microbial analysis.</li>
                    <li>🌾 <b>Organic Certification Assistance:</b> Full guidance for NPOP & Jaivik Bharat organic certification.</li>
                    <li>💰 <b>Guaranteed Buyback Guarantee:</b> Fair price remuneration paid directly into farmer bank accounts within 48 hours.</li>
                </ul>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("<div style='font-family:\"Playfair Display\", serif; font-size: 1.4rem; font-weight: 800; color: #1B4D3E; margin-bottom: 1rem;'>Join as a Partner Farmer</div>", unsafe_allow_html=True)
    with st.form("farmer_join_form"):
        name = st.text_input("Farmer Full Name")
        phone = st.text_input("Mobile Number")
        village = st.text_input("Village / District")
        acres = st.number_input("Land Size (in Acres)", min_value=1, max_value=50, value=5)
        submitted = st.form_submit_button("Submit Enrollment Request", use_container_width=True)
        if submitted:
            if name and phone and village:
                st.success(f"Thank you {name}! Our Organic Foods Agriculture Officer will contact you within 24 hours.")
            else:
                st.error("Please fill in all mandatory fields.")
