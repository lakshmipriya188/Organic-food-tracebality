"""Shopping cart & checkout page with DB integration, Order_Details copy, confirmation modal, and responsive layout."""

import streamlit as st
from config import CURRENCY
from utils.cart_manager import (
    cart_items, update_qty, remove_from_cart, cart_total, go_to
)
from utils.image_utils import get_image_src
from db_manager import checkout_order_db


def render_cart_page():
    # Show order placed success alert if set
    if st.session_state.get("order_success_msg"):
        st.balloons()
        st.success(st.session_state.order_success_msg)
        del st.session_state["order_success_msg"]

    # Top action bar
    top_col1, _ = st.columns([1.5, 4])
    with top_col1:
        if st.button("← Continue Shopping", key="cart_continue_top", use_container_width=True):
            st.session_state.show_confirm_dialog = False
            go_to("home")
            st.rerun()

    st.markdown(
        """
        <div style="font-family:'Poppins', sans-serif; font-size:0.82rem; font-weight:700; color:#16A34A; letter-spacing:2px; text-transform:uppercase; margin-top:0.8rem; margin-bottom:4px;">
            ORGANIC FOOD TRACEABILITY SYSTEM
        </div>
        <div style="font-family:'Poppins', sans-serif; font-size:2rem; font-weight:700; color:#1B4D3E; margin-bottom:1.5rem;">
            Shopping Cart & Checkout 🛒
        </div>
        """,
        unsafe_allow_html=True
    )

    items = cart_items()

    if not items:
        st.info("Your cart is empty. Explore our organic millets, cold pressed oils, and farm staples from the home page!")
        
        # Checkout buttons disabled state
        st.markdown("<hr style='border:0; height:1px; background:#E2E9E3; margin: 2rem 0 1.5rem 0;'>", unsafe_allow_html=True)
        btn_c1, btn_c2 = st.columns([1, 1])
        with btn_c1:
            if st.button("← Continue Shopping", key="cart_continue_empty", use_container_width=True):
                st.session_state.show_confirm_dialog = False
                go_to("home")
                st.rerun()
        with btn_c2:
            st.button("🚀 Proceed to Checkout", key="cart_checkout_disabled", disabled=True, use_container_width=True)
        return

    # Total accumulator variables
    total_mrp = 0.0
    total_discount = 0.0

    st.markdown("<div style='font-family:\"Poppins\", sans-serif; font-size:1.15rem; font-weight:700; color:#1B4D3E; margin-bottom:1rem;'>Cart Items</div>", unsafe_allow_html=True)

    for item in items:
        product = item["product"]
        qty = item["qty"]
        img_src = get_image_src(product.image_url)
        
        # Calculate item price components
        mrp_per_unit = float(product.original_price) if getattr(product, 'original_price', None) and product.original_price > product.price else float(product.price)
        disc_pct = float(getattr(product, 'discount_pct', 0.0) or 0.0)
        disc_amt_per_unit = round((mrp_per_unit * disc_pct) / 100.0, 2)
        final_price_per_unit = round(mrp_per_unit - disc_amt_per_unit, 2)

        item_total_mrp = mrp_per_unit * qty
        item_total_discount = disc_amt_per_unit * qty
        item_final_total = final_price_per_unit * qty

        total_mrp += item_total_mrp
        total_discount += item_total_discount

        category_name = getattr(product, 'category_name', None) or product.category_slug.title()
        p_unit = getattr(product, 'unit', 'kg')

        # Clean White Card Layout
        st.markdown(
            """
            <div style="
                background: #FFFFFF;
                border: 1px solid #E2E9E3;
                border-radius: 18px;
                padding: 1.4rem;
                margin-bottom: 1.2rem;
                box-shadow: 0 4px 14px rgba(0, 0, 0, 0.03);
            ">
            """,
            unsafe_allow_html=True
        )

        col_img, col_details, col_qty, col_actions = st.columns([1.2, 3.8, 2.2, 1.2])

        with col_img:
            st.markdown(
                f"""
                <img src="{img_src}" style="width: 100%; height: 120px; object-fit: cover; border-radius: 12px; border: 1px solid #F0F4F1;">
                """,
                unsafe_allow_html=True
            )

        with col_details:
            st.markdown(f"<div style='font-family:\"Poppins\", sans-serif; font-weight:700; font-size:1.1rem; color:#0F291E; margin-bottom: 4px;'>{product.name}</div>", unsafe_allow_html=True)
            st.markdown(f"<div style='font-size:0.85rem; color:#4A6B5D; margin-bottom: 8px;'>Category: <b>{category_name}</b> | Base Unit: <b>{p_unit}</b> | Variant: <b>{item['variant']}</b></div>", unsafe_allow_html=True)
            
            # Normal black text on white background with measurement unit
            st.markdown(
                f"""
                <div style="font-size:0.88rem; color:#0F291E; line-height:1.6;">
                    <div>Price Before Discount: <b>{CURRENCY}{mrp_per_unit:,.2f}</b> / {p_unit}</div>
                    <div>Discount (%): <b>{int(disc_pct)}%</b></div>
                    <div>Discount Amount: <b>{CURRENCY}{disc_amt_per_unit:,.2f}</b> / {p_unit}</div>
                    <div>Final Price (after discount): <b>{CURRENCY}{final_price_per_unit:,.2f}</b> / {p_unit}</div>
                </div>
                """,
                unsafe_allow_html=True
            )

        with col_qty:
            st.markdown(f"<div style='font-size:0.85rem; color:#0F291E; font-weight:600; margin-bottom:6px;'>Quantity ({p_unit})</div>", unsafe_allow_html=True)
            
            # Plus / Minus Quantity Control Row
            q_minus, q_val, q_plus = st.columns([1, 1.2, 1])
            with q_minus:
                if st.button("➖", key=f"dec_{item['key']}", use_container_width=True):
                    update_qty(item['key'], qty - 1, product_id=product.id)
                    st.rerun()
            with q_val:
                st.markdown(f"<div style='text-align:center; font-weight:700; font-size:1.1rem; padding-top:6px; color:#0F291E;'>{qty} {p_unit}</div>", unsafe_allow_html=True)
            with q_plus:
                if st.button("➕", key=f"inc_{item['key']}", use_container_width=True):
                    update_qty(item['key'], qty + 1, product_id=product.id)
                    st.rerun()

            st.markdown(f"<div style='font-size:0.82rem; color:#0F291E; margin-top:8px; text-align:center;'>Subtotal: <b>{CURRENCY}{item_final_total:,.2f}</b></div>", unsafe_allow_html=True)

        with col_actions:
            st.write("")
            if st.button("🗑️ Remove", key=f"rm_{item['key']}", use_container_width=True):
                remove_from_cart(item['key'], product_id=product.id)
                st.rerun()

        st.markdown("</div>", unsafe_allow_html=True)

    final_payable = max(0.0, total_mrp - total_discount)

    st.markdown("<hr style='border:0; height:1px; background:#E2E9E3; margin: 2rem 0 1.5rem 0;'>", unsafe_allow_html=True)

    # Price Summary Section
    st.markdown("<div style='font-family:\"Poppins\", sans-serif; font-size:1.3rem; font-weight:700; color:#1B4D3E; margin-bottom:1rem;'>Checkout Summary</div>", unsafe_allow_html=True)

    col_summary_details, col_final_highlight = st.columns([1.5, 1])

    with col_summary_details:
        st.markdown(
            f"""
            <div style="
                background: #FFFFFF;
                border: 1px solid #E2E9E3;
                border-radius: 18px;
                padding: 1.5rem;
                box-shadow: 0 4px 14px rgba(0, 0, 0, 0.03);
            ">
                <div style="display:flex; justify-content:space-between; margin-bottom: 10px; font-size: 1rem; color: #0F291E;">
                    <span>Total MRP (Price Before Discount):</span>
                    <b>{CURRENCY}{total_mrp:,.2f}</b>
                </div>
                <div style="display:flex; justify-content:space-between; margin-bottom: 10px; font-size: 1rem; color: #0F291E;">
                    <span>Total Discount:</span>
                    <b style="color: #0F291E;">- {CURRENCY}{total_discount:,.2f}</b>
                </div>
                <div style="display:flex; justify-content:space-between; margin-bottom: 4px; font-size: 0.88rem; color: #4A6B5D;">
                    <span>Calculation:</span>
                    <span>Total MRP − Total Discount</span>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col_final_highlight:
        # Green highlighted section for Final Payable Amount (bold text, larger than all other prices)
        st.markdown(
            f"""
            <div style="
                background: linear-gradient(135deg, #DCFCE7 0%, #F0FDF4 100%);
                border: 2px solid #86EFAC;
                border-radius: 18px;
                padding: 1.4rem;
                text-align: center;
                box-shadow: 0 6px 20px rgba(34, 197, 94, 0.12);
            ">
                <div style="font-family: 'Poppins', sans-serif; font-size: 0.82rem; font-weight: 700; color: #166534; letter-spacing: 1.5px; text-transform: uppercase; margin-bottom: 4px;">
                    FINAL PAYABLE AMOUNT
                </div>
                <div style="font-family: 'Poppins', sans-serif; font-size: 2.3rem; font-weight: 800; color: #15803D; line-height: 1.1;">
                    {CURRENCY}{final_payable:,.2f}
                </div>
                <div style="font-size: 0.78rem; color: #166534; margin-top: 4px; font-weight: 600;">
                    ✅ Includes all taxes & free organic express delivery
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.markdown("<div style='margin-bottom: 1.5rem;'></div>", unsafe_allow_html=True)

    # 1 EXTRA NOTIFICATION ON SCREEN TO CONFIRM OR RETURN TO CART
    if st.session_state.get("show_confirm_dialog"):
        # Format item list summary with units
        item_summary_lines = "<br>".join([
            f"• <b>{it['product'].name}</b>: {it['qty']} {getattr(it['product'], 'unit', 'kg')} @ {CURRENCY}{it['product'].price:,.2f}/{getattr(it['product'], 'unit', 'kg')}"
            for it in items
        ])
        st.markdown(
            f"""
            <div style="
                background: #FFFFFF;
                border: 2px solid #22C55E;
                border-radius: 20px;
                padding: 1.8rem;
                margin-top: 1rem;
                margin-bottom: 1.5rem;
                box-shadow: 0 10px 30px rgba(34, 197, 94, 0.15);
                text-align: center;
            ">
                <div style="font-size: 2.2rem; margin-bottom: 0.4rem;">🔔</div>
                <div style="font-family: 'Poppins', sans-serif; font-size: 1.35rem; font-weight: 700; color: #1B4D3E;">
                    Order Confirmation Prompt
                </div>
                <div style="font-size: 0.95rem; color: #4A6B5D; margin: 0.6rem 0 0.8rem 0; line-height: 1.5;">
                    Are you sure you want to place this order for <b>{CURRENCY}{final_payable:,.2f}</b>?
                </div>
                <div style="font-size: 0.88rem; color: #0F291E; text-align: left; background: #F8FAF8; border: 1px solid #E2E9E3; border-radius: 12px; padding: 0.8rem 1.2rem; margin-bottom: 1rem;">
                    {item_summary_lines}
                </div>
                <div style="font-size: 0.82rem; color: #166534;">
                    All items will be recorded into the <code>Order_Details</code> database table with date & time.
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

        conf_col1, conf_col2 = st.columns([1, 1])
        with conf_col1:
            if st.button("✅ Confirm Order", key="confirm_order_final", type="primary", use_container_width=True):
                user_id = st.session_state.get("user_id")
                if user_id:
                    checkout_order_db(int(user_id))
                
                # Clear session state cart
                st.session_state.cart = {}
                st.session_state.show_confirm_dialog = False
                st.session_state.order_success_msg = f"🎉 Order placed successfully for {CURRENCY}{final_payable:,.2f}! Cart items copied to Order_Details with date & time."
                st.rerun()

        with conf_col2:
            if st.button("↩️ Return to Cart", key="return_to_cart_btn", use_container_width=True):
                st.session_state.show_confirm_dialog = False
                st.rerun()

    else:
        # Checkout Actions Row
        btn_col1, btn_col2 = st.columns([1, 1])

        with btn_col1:
            if st.button("← Continue Shopping", key="cart_continue_bottom", use_container_width=True):
                st.session_state.show_confirm_dialog = False
                go_to("home")
                st.rerun()

        with btn_col2:
            if st.button("🚀 Proceed to Checkout", key="cart_checkout_active", type="primary", use_container_width=True):
                st.session_state.show_confirm_dialog = True
                st.rerun()
