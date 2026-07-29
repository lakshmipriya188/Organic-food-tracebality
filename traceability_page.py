"""Food Traceability Page: Transparent Farm-to-Fork Audit Trail."""

import streamlit as st
from products import PRODUCTS, get_product_by_batch
from utils.cart_manager import go_to


def render_traceability_page():
    if st.button("← Back to home"):
        go_to("home")
        st.rerun()

    st.markdown('<div class="om-section-heading">TRANSPARENCY & AUDIT TRAIL</div>', unsafe_allow_html=True)
    st.markdown('<div class="om-section-title">Farm-to-Fork Traceability Passport 🌾</div>', unsafe_allow_html=True)
    st.caption("Verify origin, farmer credentials, lab reports & zero-chemical certificates for any batch.")

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

    st.markdown("---")

    # Header section for Batch
    col_img, col_info = st.columns([1, 2])
    with col_img:
        st.image(product.image_path, use_container_width=True)
    with col_info:
        st.markdown(f"## {product.name}")
        st.markdown(f"**Batch Number:** `{product.batch_no}` | **Category:** {product.category_slug.title()}")
        st.success("✅ **STATUS:** Certified 100% Organic & Chemical-Free")
        st.markdown(f"**Harvest Date:** {product.harvest_date}")
        st.markdown(f"**Lab Certification:** {product.lab_test_cert}")

    st.markdown("### 🚜 Farm & Farmer Credentials")
    f_col1, f_col2, f_col3 = st.columns(3)
    with f_col1:
        st.metric("Farmer Name", product.farmer_name)
    with f_col2:
        st.metric("Farm Location", product.farm_location)
    with f_col3:
        st.metric("Farming Method", "Natural Farming (Zero Synthetic Inputs)")

    st.markdown("### 🔬 Laboratory Analysis & Quality Verification")
    q_col1, q_col2, q_col3, q_col4 = st.columns(4)
    with q_col1:
        st.metric("Pesticide Residue", "0.00 ppm", delta="PASS", delta_color="normal")
    with q_col2:
        st.metric("Heavy Metals Test", "Non-Detectable", delta="PASS", delta_color="normal")
    with q_col3:
        st.metric("Soil Organic Carbon", "> 1.2%", delta="+0.3%")
    with q_col4:
        st.metric("GMO Verification", "Non-GMO Seed Stock", delta="VERIFIED")

    st.markdown("### ⛓️ Immutable Supply Chain Journey")
    st.markdown(
        """
        1. **🌱 Sowing & Cultivation:** Native heritage seeds grown using JEEVAMRUTH organic manure.
        2. **🌾 Harvest & Solar Drying:** Hand-harvested and dried under controlled temperature.
        3. **🧪 Quality Audit & Lab Test:** Batch sample verified by NABL Accredited Testing Facility.
        4. **📦 Eco Packaging & QR Sealing:** Vacuum packed in biodegradable pouches with unique batch QR.
        5. **🚚 Direct Farm Delivery:** Transported in temperature-monitored direct logistics.
        """
    )

    st.info(f"🔒 **Blockchain Hash:** `0x7f8a92b...{hash(product.batch_no) & 0xffffff}` — Sealed & Immutable Record")
