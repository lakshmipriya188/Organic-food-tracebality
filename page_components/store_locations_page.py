"""Physical store locations guide across Bengaluru and Mandya for Organic Foods."""

import streamlit as st
from utils.cart_manager import go_to

STORES = [
    {
        "name": "Organic Foods Flagship Store - Indiranagar",
        "address": "100 Feet Rd, 12th Main Rd, HAL 2nd Stage, Indiranagar, Bengaluru, Karnataka 560038",
        "timing": "8:00 AM – 9:30 PM",
        "phone": "+91 95909 22001",
    },
    {
        "name": "Organic Foods Store - Jayanagar 4th Block",
        "address": "33rd Cross Rd, Near Maiya's, 4th Block, Jayanagar, Bengaluru, Karnataka 560011",
        "timing": "8:00 AM – 9:00 PM",
        "phone": "+91 95909 22002",
    },
    {
        "name": "Organic Foods Store - HSR Layout",
        "address": "Sector 7, 27th Main Rd, HSR Layout, Bengaluru, Karnataka 560102",
        "timing": "8:30 AM – 9:30 PM",
        "phone": "+91 95909 22003",
    },
    {
        "name": "Organic Foods Farm Store & Restaurant - Mandya Highway",
        "address": "NH 275, Bengaluru-Mysuru Expressway, Mandya, Karnataka 571401",
        "timing": "7:00 AM – 10:00 PM",
        "phone": "+91 95909 22000",
    },
]


def render_store_locations_page():
    if st.button("← Back to home"):
        go_to("home")
        st.rerun()

    st.markdown(
        """
        <div style="font-family:'Poppins', sans-serif; font-size:0.82rem; font-weight:700; color:#16A34A; letter-spacing:2px; text-transform:uppercase; margin-bottom:4px;">
            OUR RETAIL OUTLETS
        </div>
        <div style="font-family:'Poppins', sans-serif; font-size:2rem; font-weight:700; color:#1B4D3E; margin-bottom:0.5rem;">
            Store Locations 📍
        </div>
        <div style="color:#4A6B5D; margin-bottom:1.5rem; font-size:0.95rem;">
            Visit our physical retail outlets and farm restaurants for fresh daily organic produce and traditional dining.
        </div>
        """,
        unsafe_allow_html=True
    )

    for s in STORES:
        st.markdown(
            f"""
            <div style="
                background: #FFFFFF;
                border: 1px solid #E2E9E3;
                border-radius: 18px;
                padding: 1.4rem;
                margin-bottom: 1.2rem;
                box-shadow: 0 6px 18px rgba(27, 77, 62, 0.04);
            ">
                <div style="font-size: 1.15rem; font-weight: 800; color: #1B4D3E; margin-bottom: 6px;">{s['name']}</div>
                <div style="color: #4A6B5D; margin-bottom: 8px; font-size: 0.92rem;">📍 {s['address']}</div>
                <div style="font-size: 0.88rem; color: #166534; font-weight: 600;">⏰ <b>Timings:</b> {s['timing']} &nbsp;|&nbsp; 📞 <b>Phone:</b> {s['phone']}</div>
            </div>
            """,
            unsafe_allow_html=True
        )
