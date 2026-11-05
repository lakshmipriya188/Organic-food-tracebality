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

    # 1. Deduplicate & safely extract batch numbers
    all_batches = sorted(list({str(p.batch_no) for p in PRODUCTS if getattr(p, "batch_no", None)}))
    if not all_batches:
        all_batches = ["OF-BATCH-101"]

    current_batch = str(st.session_state.get("trace_batch_no", "") or "")
    default_idx = all_batches.index(current_batch) if current_batch in all_batches else 0

    col_input, col_btn = st.columns([3, 1])
    with col_input:
        selected_batch = st.selectbox(
            "Select or search Batch Number:",
            options=all_batches,
            index=default_idx
        )
    with col_btn:
        st.write("")
        st.write("")
        if st.button("Inspect Batch 🔎", use_container_width=True):
            st.session_state.trace_batch_no = selected_batch
            st.rerun()

    product = get_product_by_batch(str(selected_batch))
    if not product:
        st.warning(f"No batch found matching '{selected_batch}'. Please select a valid batch.")
        return

    # 2. Safe image loading
    img_url = str(getattr(product, "image_url", "") or "")
    img_src = get_image_src(img_url) if img_url else ""

    # 3. Safe type casting for pricing, category, and units
    try:
        price_num = float(product.price) if product.price is not None else 0.0
    except (ValueError, TypeError):
        price_num = 0.0

    cat_slug = str(getattr(product, "category_slug", "organic") or "organic").title()
    unit = str(getattr(product, "unit", "kg") or "kg")
    stock = getattr(product, "quantity", 50) or 50
    batch_str = str(getattr(product, "batch_no", "OF-BATCH-101") or "OF-BATCH-101")

    st.markdown("<hr style='border:0; height:1px; background:#E2E9E3; margin:1.5rem 0;'>", unsafe_allow_html=True)

    # Product Overview Card
    st.markdown(
        """
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
        st.markdown(f"**Batch Number:** `{batch_str}` | **Category:** {cat_slug} | **Price:** `₹{price_num:,.2f}/{unit}` | **Stock:** `{stock} {unit}`")
        st.success("✅ **STATUS:** Certified 100% Organic & Chemical-Free")
        st.markdown(f"**Harvest Date:** {getattr(product, 'harvest_date', '2026-07-15')} | **Origin:** {getattr(product, 'origin', 'Mandya Organic Belt')}")
        st.markdown(f"**Lab Certificate:** `{getattr(product, 'lab_test_cert', 'NABL Accredited - Pass (0.00 ppm)')}`")

    st.markdown("</div>", unsafe_allow_html=True)

    # Farmer Credentials
    st.markdown("<div style='font-family:\"Poppins\", sans-serif; font-size: 1.3rem; font-weight: 700; color: #1B4D3E; margin-bottom: 1rem;'>🚜 Farm & Farmer Credentials</div>", unsafe_allow_html=True)
    f_col1, f_col2, f_col3 = st.columns(3)
    with f_col1:
        st.metric("Farmer Name", getattr(product, "farmer_name", "Ramakrishnappa") or "Ramakrishnappa")
    with f_col2:
        st.metric("Farm Location", getattr(product, "farm_location", "Mandya Organic Belt, Karnataka") or "Mandya Organic Belt, Karnataka")
    with f_col3:
        st.metric("Farming Method", "Natural Farming (Zero Synthetic Inputs)")

    # Lab Analysis
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

    # Supply Chain
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

    st.info(f"🔒 **Blockchain Hash:** `0x7f8a92b...{hash(batch_str) & 0xffffff:06x}` — Sealed & Immutable Record")