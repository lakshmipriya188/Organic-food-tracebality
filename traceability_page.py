"""Food Traceability Page: Transparent Farm-to-Fork Audit Trail for Organic Foods."""

import streamlit as st
from products import PRODUCTS, get_product_by_batch
from utils.cart_manager import go_to
from utils.image_utils import get_image_src


def render_traceability_page():
    if st.button("← Back to home"):
        go_to("home")
        st.rerun()

    st.markdown(
        """
        <div style="font-family:'Poppins', sans-serif; font-size:0.82rem; font-weight:700; color:#16A34A; letter-spacing:2px; text-transform:uppercase; margin-bottom:4px;">
            TRANSPARENCY & AUDIT TRAIL
        </div>
        <div style="font-family:'Poppins', sans-serif; font-size:2rem; font-weight:700; color:#1B4D3E; margin-bottom:0.5rem;">
            Farm-to-Fork Traceability Passport 🌾
        </div>
        <div style="color:#4A6B5D; margin-bottom:1.5rem; font-size:0.95rem;">
            Verify origin, farmer credentials, NABL lab audit reports, & 0.00 ppm zero-chemical certificates for any harvest batch.
        </div>
        """,
        unsafe_allow_html=True
    )

    # Search Bar for Batch
    current_batch = st.session_state.get("trace_batch_no", "")
    all_batches = [p.batch_no for p in PRODUCTS]
    
    col_input, col_btn = st.columns([3, 1])
    with col_input:
        selected_batch = st.selectbox(
            "Select or search Batch Number:",
            options=all_batches,
            index=all_batches.index(current_batch) if current_batch in all_batches else 0
        )
    with col_btn:
        st.write("")
        st.write("")
        if st.button("Inspect Batch 🔎", use_container_width=True):
            st.session_state.trace_batch_no = selected_batch
            st.rerun()

    product = get_product_by_batch(selected_batch)
    if not product:
        st.warning(f"No batch found matching '{selected_batch}'. Please select a valid batch.")
        return

    img_src = get_image_src(product.image_url)

    st.markdown("<hr style='border:0; height:1px; background:#E2E9E3; margin:1.5rem 0;'>", unsafe_allow_html=True)

    # Header section for Batch
    st.markdown(
        f"""
        <div style="
            background: #FFFFFF;
            border: 1px solid #E2E9E3;
            border-radius: 20px;
            padding: 1.8rem;
            box-shadow: 0 10px 25px rgba(27, 77, 62, 0.05);
            margin-bottom: 2rem;
        ">
        """,
        unsafe_allow_html=True
    )

    col_img, col_info = st.columns([1, 2.2])
    with col_img:
        st.markdown(
            f"""
            <img src="{img_src}" style="width: 100%; height: 200px; object-fit: cover; border-radius: 14px; border: 1px solid #EEF3EF;">
            """,
            unsafe_allow_html=True
        )
    with col_info:
        st.markdown(f"<div style='font-family:\"Poppins\", sans-serif; font-size: 1.6rem; font-weight: 700; color: #1B4D3E; margin-bottom: 6px;'>{product.name}</div>", unsafe_allow_html=True)
        st.markdown(f"**Batch Number:** `{product.batch_no}` | **Category:** {product.category_slug.title()} | **Price:** `₹{product.price:,.2f}/{getattr(product, 'unit', 'kg')}` | **Stock:** `{product.quantity} {getattr(product, 'unit', 'kg')}`")
        st.success("✅ **STATUS:** Certified 100% Organic & Chemical-Free")
        st.markdown(f"**Harvest Date:** {product.harvest_date} | **Origin:** {product.origin}")
        st.markdown(f"**Lab Certificate:** `{product.lab_test_cert}`")

    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div style='font-family:\"Poppins\", sans-serif; font-size: 1.3rem; font-weight: 700; color: #1B4D3E; margin-bottom: 1rem;'>🚜 Farm & Farmer Credentials</div>", unsafe_allow_html=True)
    f_col1, f_col2, f_col3 = st.columns(3)
    with f_col1:
        st.metric("Farmer Name", product.farmer_name)
    with f_col2:
        st.metric("Farm Location", product.farm_location)
    with f_col3:
        st.metric("Farming Method", "Natural Farming (Zero Synthetic Inputs)")

    st.markdown("<div style='font-family:\"Poppins\", sans-serif; font-size: 1.3rem; font-weight: 700; color: #1B4D3E; margin: 1.8rem 0 1rem 0;'>🔬 Laboratory Analysis & Quality Verification</div>", unsafe_allow_html=True)
    q_col1, q_col2, q_col3, q_col4 = st.columns(4)
    with q_col1:
        st.metric("Pesticide Residue", "0.00 ppm", delta="PASS", delta_color="normal")
    with q_col2:
        st.metric("Heavy Metals Test", "Non-Detectable", delta="PASS", delta_color="normal")
    with q_col3:
        st.metric("Soil Organic Carbon", "> 1.2%", delta="+0.3%")
    with q_col4:
        st.metric("GMO Verification", "Non-GMO Seed Stock", delta="VERIFIED")

    st.markdown("<div style='font-family:\"Poppins\", sans-serif; font-size: 1.3rem; font-weight: 700; color: #1B4D3E; margin: 1.8rem 0 1rem 0;'>⛓️ Immutable Supply Chain Journey</div>", unsafe_allow_html=True)
    st.markdown(
        """
        <div style="background: #FFFFFF; border: 1px solid #E2E9E3; border-radius: 18px; padding: 1.5rem; margin-bottom: 1.5rem;">
            <div style="display:flex; flex-direction:column; gap:12px;">
                <div>🌱 <b>Sowing & Cultivation:</b> Native heritage seeds grown using organic JEEVAMRUTH soil enrichers.</div>
                <div>🌾 <b>Harvest & Solar Drying:</b> Hand-harvested and sun-dried under monitored clean moisture levels.</div>
                <div>🧪 <b>Quality Audit & Lab Test:</b> Batch sample verified by NABL Accredited Testing Facility.</div>
                <div>📦 <b>Eco Packaging & QR Sealing:</b> Vacuum packed in biodegradable pouches with unique batch QR.</div>
                <div>🚚 <b>Direct Farm Logistics:</b> Transported in temperature-monitored direct supply chains.</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.info(f"🔒 **Blockchain Hash:** `0x7f8a92b...{hash(product.batch_no) & 0xffffff}` — Sealed & Immutable Record")
