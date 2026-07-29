"""Physical store locations guide across Bengaluru and Mandya."""

import streamlit as st
from utils.cart_manager import go_to

STORES = [
    {
        "name": "Organic Mandya Flagship Store - Indiranagar",
        "address": "100 Feet Rd, 12th Main Rd, HAL 2nd Stage, Indiranagar, Bengaluru, Karnataka 560038",
        "timing": "8:00 AM – 9:30 PM",
        "phone": "+91 95909 22001",
    },
    {
        "name": "Organic Mandya Store - Jayanagar 4th Block",
        "address": "33rd Cross Rd, Near Maiya's, 4th Block, Jayanagar, Bengaluru, Karnataka 560011",
        "timing": "8:00 AM – 9:00 PM",
        "phone": "+91 95909 22002",
    },
    {
        "name": "Organic Mandya Store - HSR Layout",
        "address": "Sector 7, 27th Main Rd, HSR Layout, Bengaluru, Karnataka 560102",
        "timing": "8:30 AM – 9:30 PM",
        "phone": "+91 95909 22003",
    },
    {
        "name": "Organic Mandya Farm Store & Restaurant - Mandya Highway",
        "address": "NH 275, Bengaluru-Mysuru Expressway, Mandya, Karnataka 571401",
        "timing": "7:00 AM – 10:00 PM",
        "phone": "+91 95909 22000",
    },
]


def render_store_locations_page():
    if st.button("← Back to home"):
        go_to("home")
        st.rerun()

    st.markdown('<div style="font-size:0.85rem; font-weight:800; color:#00472B; letter-spacing:2px;">OUR OUTLETS</div>', unsafe_allow_html=True)
    st.markdown('<div style="font-size:2rem; font-weight:800; color:#00472B; margin-bottom:1.5rem;">Store Locations 📍</div>', unsafe_allow_html=True)
    st.write("Visit our physical retail outlets and farm restaurants for fresh daily organic produce and traditional dining.")

    for s in STORES:
        st.markdown(
            f"""
            <div style="background:#F3F6F3; border-radius:16px; padding:1.2rem; margin-bottom:1rem;">
                <div style="font-size:1.1rem; font-weight:800; color:#00472B; margin-bottom:4px;">{s['name']}</div>
                <div style="color:#556B60; margin-bottom:6px;">📍 {s['address']}</div>
                <div style="font-size:0.85rem; color:#00472B;">⏰ <b>Timings:</b> {s['timing']} | 📞 <b>Phone:</b> {s['phone']}</div>
            </div>
            """,
            unsafe_allow_html=True
        )
